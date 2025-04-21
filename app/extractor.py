# extractor.py

import re
from datetime import datetime
from dateutil import parser
import parsedatetime

cal = parsedatetime.Calendar()
def extract_booking_info(message):
    import re
    from dateutil import parser

    print(f"Extracting from message: {message}")

    name_pattern = r'\b(?:i am|i\'m|my name is|name is|for|under)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)'
    service_pattern = r'\b(massage|facial|manicure|pedicure|hair cut)\b'
    date_pattern = r'\b(?:on\s+)?([A-Z]?[a-z]+\s+\d{1,2}(?:,?\s*\d{4})?)'
    time_pattern = r'(\d{1,2}(:\d{2})?\s*(am|pm|AM|PM))'

    name_match = re.search(name_pattern, message, re.IGNORECASE)
    service_match = re.search(service_pattern, message, re.IGNORECASE)
    date_match = re.search(date_pattern, message)
    time_match = re.search(time_pattern, message)

    name = name_match.group(1).title() if name_match else None
    service = service_match.group(1) if service_match else None
    date = None
    time = None

    time_struct, parse_status = cal.parse(message)
    if parse_status:
        parsed_dt = datetime(*time_struct[:6])
        date = parsed_dt.strftime("%B %d, %Y")
        time = parsed_dt.strftime("%I:%M %p")

    if time_match:
        time = time_match.group(1)

    extracted = {
        "name": name,
        "service": service,
        "date": date,
        "time": time
    }

    print("DEBUG - Extracted Info:", extracted)
    return extracted
