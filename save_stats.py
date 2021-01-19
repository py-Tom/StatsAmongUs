import datetime
from img_processing import process_stats
from db_operations import (
    new_entry,
    update_entry,
    select_entry,
    select_table,
    remove_entry,
)


def save_stats(file, user):
    now = datetime.datetime.now()
    time = now.strftime("%d.%m.%Y %H:%M:%S")
    stats = str(process_stats(file))  # change dictionary to string
    new_user = False

    try:
        a = select_entry(user)
        if a == None:
            new_user = True
    except TypeError:
        new_user = True

    if new_user:
        new_entry(user, time, stats)
    else:
        update_entry(user, time, stats)

    return None
