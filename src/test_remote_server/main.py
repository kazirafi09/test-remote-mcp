from datetime import date, datetime
import random
from fastmcp import FastMCP

mcp = FastMCP("Custom-Tools-Server")

@mcp.tool()
def age_calculator(birthday: str) -> dict:
    """
    Calculate age in years and days given a birthday in DD-MM-YYYY format.
    """
    date_format = "%d-%m-%Y"
    birth_date = datetime.strptime(birthday, date_format).date()
    today_date = date.today()

    if today_date < birth_date:
        raise ValueError("Today's date cannot be earlier than birthday.")

    years = today_date.year - birth_date.year
    try:
        last_birthday = birth_date.replace(year=today_date.year)
    except ValueError:
        last_birthday = birth_date.replace(year=today_date.year, day=28)

    if last_birthday > today_date:
        years -= 1
        try:
            last_birthday = birth_date.replace(year=today_date.year - 1)
        except ValueError:
            last_birthday = birth_date.replace(year=today_date.year - 1, day=28)

    days = (today_date - last_birthday).days

    return {
        "age": f"{years} years, {days} days",
        "years": years,
        "days": days,
    }

@mcp.tool()
def random_number(min_value: int, max_value: int) -> int:
    """Generate a random integer between min_value and max_value (inclusive).
    
    Args:
        min_value: Minimum integer
        max_value: Maximum integer
    """
    if min_value > max_value:
        min_value, max_value = max_value, min_value
    return random.randint(min_value, max_value)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)