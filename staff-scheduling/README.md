# Staff Scheduling System

An intelligent Python application that automates staff scheduling by assigning operators (OT) and assistants to work on holidays and weekends. The system handles holiday conflicts, leave requests, and ensures fair rotation among staff members.

## Features

- **Automated Scheduling**: Generates 90-day schedules for weekends and public holidays
- **Smart Conflict Resolution**: Automatically handles staff leave and holiday requests
- **Public Holiday Integration**: Fetches Hong Kong public holidays from 1823.gov.hk API
- **Alphabetical Rotation**: Ensures fair distribution of shifts among staff members
- **Excel Integration**: Reads staff data from Excel and exports schedules to Excel format
- **Holiday Blocking**: Staff can specify unavailable dates with automatic conflict detection
- **Bidirectional Expansion**: Intelligently expands blocked dates to avoid isolated work days

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Input File Format](#input-file-format)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Output](#output)

## Installation

1. **Clone the repository**:
   ```bash
   git clone
   cd staff-scheduling
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your staff data**:
   - Place your `staff_list.xlsx` file in the `data/` directory
   - See [Input File Format](#input-file-format) for the required structure

## Usage

Run the application from the project root:

```bash
python src/main.py
```

The program will:
1. Prompt you for the last assigned OT and Assistant (press Enter if first time)
2. Load staff data from `data/staff_list.xlsx`
3. Fetch public holidays from the 1823.gov.hk API
4. Generate a 90-day schedule
5. Export the schedule to `schedule.xlsx` in the current directory

### Example Session

```
If you dont know the last assigned OT and Assistant or It is the first time using this program. Please press Enter for the following input value
Last assigned OT: John Doe
Last assigned Assistant: Jane Smith
Load staff data from an Excel file and return a list of staff members.
Successfully fetched 35 public holidays from 1823.gov.hk.
Schedule saved to schedule.xlsx
```

## Input File Format

Your `staff_list.xlsx` must contain the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| **name** | Staff member's full name | John Doe |
| **position** | Either "OT" or "Assistant" | OT |
| **holiday** | Regular holiday dates | (2025-01-15), (2025-02-10, 2025-02-15) |
| **special holiday** | Additional blocked dates | (2025-03-20) |

### Date Format Rules

- Single date: `(YYYY-MM-DD)`
- Date range: `(YYYY-MM-DD, YYYY-MM-DD)`
- Multiple entries: `(2025-01-15), (2025-02-10, 2025-02-15)`

### Sample Excel Data

| name | position | holiday | special holiday |
|------|----------|---------|-----------------|
| John Doe | OT | (2025-01-15) | (2025-03-20) |
| Jane Smith | Assistant | (2025-02-10, 2025-02-15) | |
| Bob Wilson | OT | | (2025-01-25) |

## How It Works

### 1. Staff Rotation
- Staff are sorted alphabetically by name
- Assignments rotate in order, ensuring fair distribution
- Rotation continues from the last assigned person (to maintain fairness across runs)

### 2. Holiday Detection
- Fetches real-time public holidays from Hong Kong's official API
- Includes all weekends (Saturday and Sunday) automatically
- Falls back to hardcoded 2025 holidays if API is unavailable

### 3. Conflict Resolution
- Checks each staff member's holiday and special holiday dates
- Skips unavailable staff and moves to the next person in rotation
- Uses bidirectional expansion to avoid isolated work days between holidays

### 4. Bidirectional Expansion Algorithm
When a staff member requests leave, the system intelligently expands the blocked period to include work days that would be isolated between holidays. This prevents situations where someone works one day between two holidays.

Example: If a staff member has leave on Jan 15 and Jan 17, and Jan 16 is a work day, the system will automatically block Jan 16 as well.

## Project Structure

```
staff-scheduling/
├── src/
│   ├── main.py                    # Application entry point
│   ├── scheduler.py               # Core scheduling logic and Scheduler class
│   └── utils/
│       ├── __init__.py
│       ├── excel_handler.py       # Excel file reading functions
│       └── roster_generator.py    # Daily roster generation algorithms
├── data/
│   └── staff_list.xlsx           # Input: Staff data with positions and holidays
├── requirements.txt               # Python package dependencies
├── schedule.xlsx                  # Output: Generated schedule (created after run)
└── README.md                      # This file
```

## Requirements

- Python 3.7+
- pandas
- openpyxl
- requests

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## Output

The application generates `schedule.xlsx` with three columns:

| Date | Ot | Assistant |
|------|-----|-----------|
| 2025-01-06 | John Doe | Jane Smith |
| 2025-01-07 | Bob Wilson | Alice Johnson |
| ... | ... | ... |

The schedule covers the next 90 days of weekends and public holidays.

## Error Handling

The system handles several edge cases:

- **Insufficient Staff**: Raises error if less than 1 OT and 1 Assistant available
- **All Staff Unavailable**: Raises error if no staff available for a specific date
- **API Failure**: Falls back to hardcoded 2025 Hong Kong public holidays
- **Missing Excel File**: Shows clear error message with expected file path

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.