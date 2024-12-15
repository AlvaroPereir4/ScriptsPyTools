from bson.objectid import ObjectId
from datetime import datetime


start_id = ObjectId.from_datetime(datetime(2024, 12, 13, 0, 0, 0))
end_id = ObjectId.from_datetime(datetime(2024, 12, 13, 23, 59, 59))

print(start_id, end_id)
