
# Zendesk Inactive User Downgrade Script

This script identifies and downgrades inactive agents in Zendesk who have not logged in for a specified period (default is 45 days). It also handles users who have never logged in. Inactive agents will be downgraded to the role of "end-user," effectively removing them as light agents.

## Prerequisites

- Python 3.x
- Required Python packages:
  - `requests`
  - `pandas`

You can install the necessary packages using pip:

```bash
pip install requests pandas
```

## Setup

1. **Create a credentials dictionary:** The script requires a dictionary of your Zendesk credentials and API key. Set up the dictionary with the following format:

   ```python
   credentials = {
       "subdomain": "yourzdsubdomain",
       "email": "ZDadmin@yourorg.com",
       "api_token": "example_api_key"
   }
   ```

2. **Adjust the `active_date` variable (optional):** The script defaults to checking for users who have been inactive for 45 days. You can adjust this by changing the value of the `active_date` variable.

   ```python
   active_date = (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d')
   ```

## How to Run the Script

1. Ensure your credentials dictionary is correctly populated.
2. Run the script using your preferred Python environment.

```bash
python downgrade_inactive_users.py
```

## Script Details

- The script fetches all agents from the Zendesk API using pagination and checks their last login date.
- Agents who have not logged in since the `active_date` or have never logged in will be marked as inactive.
- The script then downgrades these inactive agents to the "end-user" role, which removes their "light agent" status.
- The script prints out the number of inactive users and logs the downgrade process.

## Example Output

```bash
Found 3 inactive users on subdomain yourzdsubdomain
Downgrading user https://yourzdsubdomain.zendesk.com/api/v2/users/12345.json
200 {'user': {'role': 'end-user'}}
```

## Troubleshooting

- **Failed to fetch data:** If the script encounters issues fetching data, it will output the status code and the full response from Zendesk for debugging purposes.
- **Key 'users' not found in the response:** This indicates a problem with the API response, and the script will print the full response for you to review.

## License

This script is provided "as-is" under the MIT License. Feel free to modify and use it according to your needs.
