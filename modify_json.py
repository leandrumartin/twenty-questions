import json


def add_items():
    with open('items.json') as f:
        items = json.load(f)

    active = True
    while active:
        new_item = {}
        print('Type "t" or "f" for each (except the name). If it is not applicable, type "f".')
        print('{')

        for key in items[0]:
            if key == "name":
                new_item[key] = input(f'\t{key}: ').strip()
            else:
                if input(f'\t{key}: ').strip().lower().startswith('t'):
                    new_item[key] = True
                else:
                    new_item[key] = False
        print('}')
        items.append(new_item)

        answer = input("\nAdd another? ")
        if not answer.lstrip().lower().startswith('y'):
            active = False

    with open('items.json', 'w') as f:
        json.dump(items, f)


def add_properties():
    with open('items.json') as f:
        items = json.load(f)

    active = True
    while active:
        new_key = input("\nNew key: ").strip()
        if new_key in items[0]:
            print("Key already exists.")
        else:
            print('\nType "t" or "f" for each.')
            for item in items:
                new_value = input(f"{item['name']}: ").strip().lower()
                if new_value == 't':
                    item[new_key] = True
                else:
                    item[new_key] = False

            answer = input("\nAdd another? ")
            if not answer.lstrip().lower().startswith('y'):
                active = False

    with open('items.json', 'w') as f:
        json.dump(items, f)


if __name__ == '__main__':
    active = True
    while active:
        lines = ["",
                 "Enter the number of what you would like to do:",
                 "",
                 "(0) Quit",
                 "(1) Add items",
                 "(2) Add properties",
                 ]
        for line in lines:
            print(line)
        num = int(input())

        if num == 0:
            active = False
        elif num == 1:
            add_items()
        elif num == 2:
            add_properties()
