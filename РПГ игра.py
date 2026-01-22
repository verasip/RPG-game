import random

exp_lvl = {1: 0, 2: 100, 3: 300, 4: 600, 5: 1000}
items = [
    {"name": "Меч", "type": "weapon", "attack": 8},
    {"name": "Доспех", "type": "armor", "defense": 10},
    {"name": "Зелье", "type": "potion", "heal": 60},
    {"name": "Сильный меч", "type": "weapon", "attack": 15},
    {"name": "Сильный доспех", "type": "armor", "defense": 18},
]

locations = {
    "старт": {
        "name": "Начальная поляна",
        "description": "Вы на солнечной поляне. Отсюда начинается ваш путь.",
        "exits": ["лес", "пещера"],
        "type": "safe"
    },
    "лес": {
        "name": "Темный лес",
        "description": "Густой лес, где почти не видно солнца.",
        "exits": ["старт", "река", "глушь"],
        "type": "enemy"
    },
    "пещера": {
        "name": "Вход в пещеру",
        "description": "Темное отверстие в скале. Изнутри доносится эхо.",
        "exits": ["старт", "подземелье"],
        "type": "chest"
    },
    "река": {
        "name": "Быстрая река",
        "description": "Шумная река с чистой водой.",
        "exits": ["лес", "мост"],
        "type": "rest"
    },
    "глушь": {
        "name": "Лесная глушь",
        "description": "Самая опасная часть леса.",
        "exits": ["лес"],
        "type": "enemy"
    },
    "подземелье": {
        "name": "Глубины пещеры",
        "description": "Сырые каменные коридоры.",
        "exits": ["пещера", "трон"],
        "type": "enemy"
    },
    "мост": {
        "name": "Старый мост",
        "description": "Древний мост через реку.",
        "exits": ["река"],
        "type": "boss"
    },
    "трон": {
        "name": "Тронный зал",
        "description": "Огромный зал с каменным троном.",
        "exits": ["подземелье"],
        "type": "final"
    },
}

player = {
    'name': '', 'level': 1, 'exp': 0, 'points': 0,
    'attack': 0, 'defense': 0, 'hp': 0, 'max_hp': 0,
    'potion_power': 0, 'inventory': [], 'equipped': {'weapon': None, 'armor': None},
    'wins': 0, 'location': 'старт', 'visited': []
}

enemy_names = ["Гоблин", "Орк", "Тролль", "Волк", "Зомби"]


def show_location():
    loc = locations[player['location']]
    print(f"\n{'=' * 40}")
    print(f"локация {loc['name']}")
    print(f"{'=' * 40}")
    print(f"{loc['description']}")

    if player['location'] not in player['visited']:
        player['visited'].append(player['location'])

    handle_location_event(loc['type'])


def handle_location_event(loc_type):
    if loc_type == "enemy":
        if random.random() < 0.7:
            start_battle()
    elif loc_type == "chest":
        if random.random() < 0.8:
            print("\n Вы нашли сундук!")
            find_item()
    elif loc_type == "rest":
        print("\n Это место для отдыха")
        rest()
    elif loc_type == "boss":
        print("\n️ Ощущается сильное зловещее присутствие...")
        start_boss_battle()
    elif loc_type == "final":
        print("\n Вы достигли финальной локации!")
        if player['wins'] >= 5:
            print(" Вы победили всех врагов и завершили игру!")
        else:
            print("Вернитесь, когда будете готовы к финальной битве.")


def rest():
    old_hp = player['hp']
    player['hp'] = player['max_hp']
    healed = player['hp'] - old_hp
    print(f"Вы отдохнули и восстановили {healed} HP")
    print(f"Теперь HP: {player['hp']}/{player['max_hp']}")


def move():
    loc = locations[player['location']]
    print(f"\nКуда идти?")

    for i, exit_name in enumerate(loc['exits'], 1):
        exit_loc = locations[exit_name]
        print(f"{i}. {exit_loc['name']} - {exit_loc['description'][:30]}...")

    try:
        choice = int(input(f"\nВыберите путь (1-{len(loc['exits'])}): ")) - 1
        if 0 <= choice < len(loc['exits']):
            player['location'] = loc['exits'][choice]
            return True
    except:
        print("Неверный выбор!")
    return False


def show_map():
    print("\n ВАШ ПУТЬ:")
    for loc_name in player['visited']:
        loc = locations[loc_name]
        mark = "локация" if loc_name == player['location'] else "✓"
        print(f"{mark} {loc['name']}")


def update_stats():
    player['attack'] = 25 + player['level'] * 2
    player['defense'] = 12 + player['level']
    player['max_hp'] = 200 + player['level'] * 20

    if player['equipped']['weapon']:
        player['attack'] += player['equipped']['weapon']['attack']
    if player['equipped']['armor']:
        player['defense'] += player['equipped']['armor']['defense']

    if player['hp'] > player['max_hp']:
        player['hp'] = player['max_hp']


def find_item():
    if random.random() < 0.6:
        item = random.choice(items).copy()
        player['inventory'].append(item)
        print(f" Нашли: {item['name']}")


def level_up():
    for lvl in range(5, player['level'], -1):
        if player['exp'] >= exp_lvl[lvl]:
            old_lvl = player['level']
            player['level'] = lvl
            player['points'] += 5
            print(f" Уровень повышен: {old_lvl} → {lvl}!")
            print(f" Очков характеристик: {player['points']}")
            break


def create_enemy(battle_num=1):
    return {
        'name': f"{random.choice(enemy_names)} {battle_num}",
        'attack': 15 + battle_num * 3,
        'defense': 8 + battle_num * 2,
        'hp': 120 + battle_num * 20,
        'max_hp': 120 + battle_num * 20
    }


def create_boss():
    return {
        'name': "КОРОЛЬ ТРОЛЛЕЙ",
        'attack': 30 + player['level'] * 5,
        'defense': 20 + player['level'] * 3,
        'hp': 300 + player['level'] * 50,
        'max_hp': 300 + player['level'] * 50
    }


def show_status():
    print(
        f"\n{player['name']}: HP {player['hp']}/{player['max_hp']} | ATK {player['attack']} | DEF {player['defense']}")


def battle(enemy, battle_num=1):
    print(f"\n{'=' * 40}")
    print(f"⚔ БОЙ С {enemy['name']}")
    print(f"{'=' * 40}")

    print(f"\n {enemy['name']}:")
    print(f"  Атака: {enemy['attack']}")
    print(f"  Защита: {enemy['defense']}")
    print(f"  Здоровье: {enemy['hp']}/{enemy['max_hp']}")

    turn = 1

    while player['hp'] > 0 and enemy['hp'] > 0:
        print(f"\n--- Ход {turn} ---")
        show_status()
        print(f"{enemy['name']}: HP {enemy['hp']}/{enemy['max_hp']}")

        print("\nВаши действия:")
        print("1. Атаковать")
        print(f"2. Использовать зелье (+{player['potion_power']} HP)")
        if player['inventory']:
            print("3. Использовать предмет из инвентаря")

        action = input("Выберите действие: ")

        if action == '1':
            damage = max(1, player['attack'] - enemy['defense'] + random.randint(0, 5))

            if random.random() < 0.2:
                damage = int(damage * 1.5)
                print(" КРИТИЧЕСКИЙ УДАР!")

            enemy['hp'] -= damage
            print(f"Вы нанесли {damage} урона!")

        elif action == '2':
            old_hp = player['hp']
            player['hp'] = min(player['max_hp'], player['hp'] + player['potion_power'])
            healed = player['hp'] - old_hp
            print(f" Вы восстановили {healed} HP")

        elif action == '3' and player['inventory']:
            print("\nВаш инвентарь:")
            for i, item in enumerate(player['inventory']):
                if item['type'] == 'potion':
                    print(f"{i + 1}. {item['name']} (+{item['heal']} HP)")

            try:
                choice = int(input("Номер зелья: ")) - 1
                if 0 <= choice < len(player['inventory']) and player['inventory'][choice]['type'] == 'potion':
                    item = player['inventory'][choice]
                    player['hp'] = min(player['max_hp'], player['hp'] + item['heal'])
                    print(f" Использовали {item['name']}!")
                    del player['inventory'][choice]
            except:
                print("Ошибка выбора!")

        if enemy['hp'] <= 0:
            print(f"\n {enemy['name']} повержен!")
            player['wins'] += 1
            exp_gained = 50 + enemy['attack']
            player['exp'] += exp_gained
            print(f" Получено {exp_gained} опыта")
            level_up()
            find_item()
            return True

        print(f"\nХод {enemy['name']}:")

        damage = max(1, enemy['attack'] - player['defense'] + random.randint(-2, 2))

        if random.random() < 0.1:
            print(f" {enemy['name']} промахнулся!")
        else:
            player['hp'] -= damage
            print(f"{enemy['name']} нанес вам {damage} урона")

        if player['hp'] <= 0:
            print(f"\n Вы проиграли в бою с {enemy['name']}!")
            return False

        turn += 1

    return False


def start_battle():
    enemy = create_enemy(player['wins'] + 1)
    if battle(enemy, player['wins'] + 1):
        print("\nВы победили! Можете продолжать путь.")
    else:
        print("\nИгра окончена.")
        exit()


def start_boss_battle():
    boss = create_boss()
    print(f"\n️ Перед вами могучий {boss['name']}!")
    if battle(boss, 999):
        print(f"\n ВЫ ПОБЕДИЛИ ФИНАЛЬНОГО БОССА!")
        print(" ИГРА ЗАВЕРШЕНА УСПЕШНО!")
        exit()


print("=" * 40)
print(" RPG ПУТЕШЕСТВИЕ")
print("=" * 40)

player['name'] = input("Введите имя персонажа: ")

update_stats()
player['hp'] = player['max_hp']
player['potion_power'] = 70

for item in items[:3]:
    player['inventory'].append(item.copy())

print(f"\n Персонаж: {player['name']}")
print(f" Уровень: {player['level']}")
print(f"️ Атака: {player['attack']}")
print(f"️ Защита: {player['defense']}")
print(f"️ Здоровье: {player['hp']}/{player['max_hp']}")
print(f" Зелье лечения: +{player['potion_power']} HP")

if player['inventory']:
    print("\n Ваши предметы:")
    for i, item in enumerate(player['inventory']):
        print(f"{i + 1}. {item['name']} ({item['type']})")

    equip = input("Экипировать предмет сейчас? (да/нет): ")
    if equip.lower() in ['да', 'д', 'y', 'yes']:
        try:
            choice = int(input("Номер предмета: ")) - 1
            if 0 <= choice < len(player['inventory']):
                item = player['inventory'][choice]
                if item['type'] == 'weapon':
                    player['equipped']['weapon'] = item
                elif item['type'] == 'armor':
                    player['equipped']['armor'] = item
                player['inventory'].remove(item)
                update_stats()
                print(f"Экипирован: {item['name']}")
        except:
            pass

print("\n" + "=" * 40)
print(" НАЧАЛО ПУТЕШЕСТВИЯ!")
print("=" * 40)

while player['hp'] > 0:
    show_location()

    print("\nЧто делать?")
    print("1. Осмотреться вокруг")
    print("2. Переместиться в другую локацию")
    print("3. Посмотреть карту")
    print("4. Проверить инвентарь")
    print("5. Посмотреть статистику")
    print("6. Выйти из игры")

    action = input("Выберите действие (1-6): ")

    if action == '1':
        print("\nВы осматриваетесь...")
        loc = locations[player['location']]
        handle_location_event(loc['type'])

    elif action == '2':
        if move():
            continue

    elif action == '3':
        show_map()

    elif action == '4':
        if player['inventory']:
            print("\n Ваш инвентарь:")
            for i, item in enumerate(player['inventory']):
                print(f"{i + 1}. {item['name']} ({item['type']})")

            equip_now = input("Экипировать предмет? (да/нет): ")
            if equip_now.lower() in ['да', 'д', 'y', 'yes']:
                try:
                    choice = int(input("Номер предмета: ")) - 1
                    if 0 <= choice < len(player['inventory']):
                        item = player['inventory'][choice]
                        if item['type'] == 'weapon':
                            if player['equipped']['weapon']:
                                player['inventory'].append(player['equipped']['weapon'])
                            player['equipped']['weapon'] = item
                        elif item['type'] == 'armor':
                            if player['equipped']['armor']:
                                player['inventory'].append(player['equipped']['armor'])
                            player['equipped']['armor'] = item
                        player['inventory'].remove(item)
                        update_stats()
                        print(f"Экипирован: {item['name']}")
                except:
                    print("Ошибка!")
        else:
            print(" Инвентарь пуст")

    elif action == '5':
        print(f"\n СТАТИСТИКА:")
        print(f" Игрок: {player['name']}")
        print(f" Уровень: {player['level']}")
        print(f" Побед: {player['wins']}")
        print(f" Опыт: {player['exp']}")
        print(f" Текущая локация: {locations[player['location']]['name']}")
        print(f"️ Посещено локаций: {len(player['visited'])}/{len(locations)}")

    elif action == '6':
        print("Спасибо за игру!")
        break

    else:
        print("Неверный выбор!")

print("\n" + "=" * 40)
print(" ИГРА ЗАВЕРШЕНА")
print("=" * 40)

print(f"\n ИТОГОВАЯ СТАТИСТИКА:")
print(f" Игрок: {player['name']}")
print(f" Уровень: {player['level']}")
print(f" Побед: {player['wins']}")
print(f" Опыт: {player['exp']}")
print(f"️ Посещено локаций: {len(player['visited'])}/{len(locations)}")
print(f" Предметов в инвентаре: {len(player['inventory'])}")

if player['wins'] >= 5:
    print("\n ВЫ СТАЛИ ЛЕГЕНДОЙ ЭТИХ ЗЕМЕЛЬ!")