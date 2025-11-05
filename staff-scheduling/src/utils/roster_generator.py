import pandas as pd
from collections import deque
from datetime import timedelta, date
from typing import List, Deque, Set

def rotate_after_item(arr, key):
    try:
        idx = next(i for i, sub in enumerate(arr) if sub[0] == key)
        return arr[idx + 1:] + arr[:idx + 1]
    except StopIteration:
        return arr

def skip_and_insert_after(d: deque) -> None:
    if len(d) < 2:
        return
    current = d.popleft()
    next_person = d.popleft()
    d.appendleft(current)
    d.appendleft(next_person)

def block_touches_holiday(block: List[date], holiday: date) -> bool:
    if len(block) == 1:
        return holiday == block[0]
    elif len(block) == 2:
        start, end = block
        if start <= holiday <= end:
            return True
        return False
    else:
        raise ValueError("block must be [date] or [start, end]")

def expand_bidirectional(relevant_dates: Set[date], work_set: Set[date]) -> Set[date]:
    expanded = relevant_dates.copy()
    changed = True

    while changed:
        changed = False
        new_additions = set()

        for work_day in work_set:
            if work_day in expanded:
                continue

            n1 = work_day + timedelta(days=1)
            n2 = work_day + timedelta(days=2)
            if (n1 in expanded and n2 in work_set) or \
               (n1 in work_set and n2 in expanded):
                new_additions.add(work_day)
                continue

            p1 = work_day - timedelta(days=1)
            p2 = work_day - timedelta(days=2)
            if (p1 in expanded and p2 in work_set) or \
               (p1 in work_set and p2 in expanded):
                new_additions.add(work_day)

        if new_additions:
            expanded.update(new_additions)
            changed = True

    return expanded

def merge_requested_with_work_holidays(
    staff_requested: List[List[date]],
    work_holidays: List[date]
) -> List[List[date]]:
    if not staff_requested:
        return []

    work_set = set(work_holidays)

    relevant_dates: Set[date] = set()

    for block in staff_requested:
        if len(block) == 1:
            d = block[0]
            relevant_dates.add(d)
            for delta in [-1, 1]:
                adj = d + timedelta(days=delta)
                if adj in work_set:
                    relevant_dates.add(adj)
        else:
            start, end = block
            for offset in range((end - start).days + 1):
                d = start + timedelta(days=offset)
                relevant_dates.add(d)
                for delta in [-1, 1]:
                    adj = d + timedelta(days=delta)
                    if adj in work_set:
                        relevant_dates.add(adj)

    relevant_dates = expand_bidirectional(relevant_dates, work_set)

    if not relevant_dates:
        return []

    dates_list = sorted(relevant_dates)
    merged: List[List[date]] = []
    cur_start = cur_end = dates_list[0]

    for d in dates_list[1:]:
        if d <= cur_end + timedelta(days=1):
            cur_end = d
        else:
            merged.append([cur_start, cur_end])
            cur_start = cur_end = d
    merged.append([cur_start, cur_end])

    return merged

def preprocess_with_holidays(input_array, holiday_list):
    for person in input_array:
        if person[2]:
            person[2] = merge_requested_with_work_holidays(person[2], holiday_list)
    return input_array

def generate_daily_roster(staff_data, day=0, holidays=[], last_assign=[]):
    if len(staff_data) < 2:
        raise ValueError("Not enough staff members to assign an operator and an assistant.")
        
    ots_array = [s for s in staff_data if s[1].lower() == 'ot']
    ots_array = preprocess_with_holidays(rotate_after_item(ots_array, last_assign[0]), holidays)
    Ots = deque(ots_array)

    assistants_array = [s for s in staff_data if s[1].lower() == 'assistant']
    assistants_array = preprocess_with_holidays(rotate_after_item(assistants_array, last_assign[1]), holidays)
    assistants = deque(assistants_array)

    if len(Ots) == 0 or len(assistants) == 0:
        raise ValueError("Need at least one Ot and one assistant for scheduling.")

    schedule = []
    for holiday in holidays:
        while Ots:
            ot = Ots[0]
            skip = any(block_touches_holiday(block, holiday) for block in ot[2])
            if skip:
                skip_and_insert_after(Ots)
            else:
                break

        while assistants:
            ass = assistants[0]
            skip = any(block_touches_holiday(block, holiday) for block in ass[2])
            if skip:
                skip_and_insert_after(assistants)
            else:
                break

        if not Ots or not assistants:
            raise ValueError(f"No available staff for {holiday}")

        schedule.append({
            'date':      holiday,
            'Ot':        Ots[0][0],
            'Assistant': assistants[0][0],
        })

        Ots.rotate(-1)
        assistants.rotate(-1)

    return schedule