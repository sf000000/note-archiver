A Python script that archives music notes shared through Instagram's notes feature to a Supabase database.

## Requirements

- Python 3.7+
- Dependencies listed in requirements.txt

## Setup

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Rename the `.env.example` file to `.env` and fill in the missing values.

## Usage

```bash
python3 main.py
```

The script will automatically check for new music notes every 10 minutes and save them to the Supabase database.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
