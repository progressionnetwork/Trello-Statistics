import json
from datetime import datetime, timedelta


def load_trello_backup(file_path):
    with open(file_path, 'r') as file:
        trello_data = json.load(file)
    return trello_data


def get_statistics(trello_data):
    lists = trello_data['lists']
    cards = trello_data['cards']

    # Number of lists
    num_lists = len(lists)

    # Number of cards
    num_cards = len(cards)

    # Number of cards per list
    cards_per_list = {lst['name']: sum(1 for card in cards if card['idList'] == lst['id']) for lst in lists}

    # Number of cards per time period
    now = datetime.now()
    last_week = now - timedelta(weeks=1)
    last_month = now - timedelta(weeks=4)
    last_year = now - timedelta(weeks=52)

    cards_last_week = sum(1 for card in cards if parse_trello_date(card['dateLastActivity']) > last_week)
    cards_last_month = sum(1 for card in cards if parse_trello_date(card['dateLastActivity']) > last_month)
    cards_last_year = sum(1 for card in cards if parse_trello_date(card['dateLastActivity']) > last_year)

    # Number of cards done per time period
    done_cards_last_week = sum(1 for card in cards if
                               parse_trello_date(card['dateLastActivity']) > last_week and card.get('dueComplete',
                                                                                                    False))
    done_cards_last_month = sum(1 for card in cards if
                                parse_trello_date(card['dateLastActivity']) > last_month and card.get('dueComplete',
                                                                                                      False))
    done_cards_last_year = sum(1 for card in cards if
                               parse_trello_date(card['dateLastActivity']) > last_year and card.get('dueComplete',
                                                                                                    False))

    # Number of cards in the "Done" list
    done_list_id = next((lst['id'] for lst in lists if lst['name'] == 'Сделано'), None)
    if done_list_id:
        done_cards = [(card['name'], parse_trello_date(card['dateLastActivity'])) for card in cards if
                      card['idList'] == done_list_id]
        cards_in_done_list = sum(1 for card in cards if card['idList'] == done_list_id)
    else:
        done_cards = []
        cards_in_done_list = 0

    # List of tasks you should do (not in the "Done" list)
    tasks_to_do = [(card['name'], card['idList']) for card in cards if card['idList'] != done_list_id]

    # Display statistics
    print(f"Number of lists: {num_lists}")
    print(f"Number of cards: {num_cards}")
    for lst, count in cards_per_list.items():
        print(f"Number of cards on list {lst}: {count}")
    print(f"Number of cards per last week: {cards_last_week}")
    print(f"Number of cards per last month: {cards_last_month}")
    print(f"Number of cards per last year: {cards_last_year}")
    print(f"Number of cards done last week: {done_cards_last_week}")
    print(f"Number of cards done last month: {done_cards_last_month}")
    print(f"Number of cards done last year: {done_cards_last_year}")
    print(f"Number of cards in the 'Done' list: {cards_in_done_list}")

    # Enumerate tasks in the "Done" list
    print("\nTasks in the 'Done' list:")
    for task, completion_date in done_cards:
        print(f"Task: {task}, Completed on: {completion_date}")

    # List of tasks you should do
    print("\nTasks you should do:")
    for task, list_id in tasks_to_do:
        list_name = next((lst['name'] for lst in lists if lst['id'] == list_id), None)
        print(f"Task: {task}, List: {list_name}")


def parse_trello_date(date_str):
    # Parse Trello date format and return datetime object
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")


if __name__ == "__main__":
    # Replace 'your_backup_file.json' with the actual path to your Trello backup JSON file
    trello_backup_file_path = r'D:\Projects\TrelloBackup\2023_12_29_backup\me\kanban 2023\kanban 2023_full.json'
    trello_data = load_trello_backup(trello_backup_file_path)
    get_statistics(trello_data)
