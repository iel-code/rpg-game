import json
import os
import time
import random

CLASSES = {
    "warrior": {
        "health": 100,
        "attack": 15,
        "defense": 10,
        "magic": 3,
        "speed": 5
    },
    "mage": {
        "health": 60,
        "attack": 8,
        "defense": 5,
        "magic": 20,
        "speed": 7
    },
    "rogue": {
        "health": 80,
        "attack": 12,
        "defense": 7,
        "magic": 5,
        "speed": 15
    }
}

ITEMS = {
    "health_potion" : {
        "name" : "Health Potion",
        "type" : "consumable",
        "value" : 30,
        "cost": 20
    },
    "strength_potion" : {
        "name" : "Strength Potion",
        "type" : "consumable",
        "value": 5,
        "cost": 30
    },
    "iron_sword" : {
        "name" : "Iron Sword",
        "type" : "weapon",
        "value" : 3,
        "cost" : 100
    },
    "diamond_sword" : {
        "name" : "Diamond Sword",
        "type" : "weapon",
        "value" : 8,
        "cost" : 170
    },
    "iron_armor" : {
        "name" : "Iron Armor",
        "type" : "armor",
        "value" : 2,
        "cost": 80
    },
    "diamond_armor" : {
        "name" : "Diamond Armor",
        "type" : "armor",
        "value" : 5,
        "cost" : 150
    }
}


def create_character():
    print("\n" + "=" * 40)
    print("⚔️  CHARACTER CREATION ⚔️")
    print("="*40)

    name = input("Enter your hero's name: ").strip()
    while not name:
        print("❌ Name cannot be empty!")
        name = input("Enter your hero's name: ").strip()
    
    print("\n=== Choose your class ===")
    print("1. Warrior (High HP, High Attack, Low Magic)")
    print("2. Mage (Low HP, Low Attack, High Magic)")
    print("3. Rogue (Balanced stats, High Speed)")

    class_choice = input("Pick a choice 1-3: ").strip()

    while class_choice not in ['1', '2', '3']:
        print("❌ Invalid choice!")
        class_choice = input("Pick a choice 1-3: ").strip()
    
    class_map = {"1": "warrior", "2": "mage", "3": "rogue"}
    chosen_class = class_map[class_choice]

    character = {
        "name": name,
        "class": chosen_class,
        "level": 1,
        "exp": 0,
        "gold": 0,
        "inventory": {},
        "equipped_weapon": None,
        "equipped_armor": None,
        "stats": CLASSES[chosen_class].copy(),
        "base_stats" : CLASSES[chosen_class].copy(),
        "max_health": CLASSES[chosen_class]['health']
    }

    display_character(character)
    
    return character

def display_character(character):
    print("\n" + "="*40)
    print("✨ CHARACTER INFO ✨")
    print("="*40)
    print(f"\nName: {character['name']}")
    print(f"Class: {character['class'].capitalize()}")
    print(f"Level: {character['level']}")
    print(f"Exp: {character['exp']}")
    print(f"Gold : {character['gold']}")

    print("\n⚔️ Equipment:")
    if character['equipped_weapon']:
        print(f"Weapon: {ITEMS[character['equipped_weapon']]['name']}")
    if character['equipped_armor']:
        print(f"Armor: {ITEMS[character['equipped_armor']]['name']}")

    weapon_bonus = 0
    armor_bonus = 0
    if character['equipped_weapon']:
        weapon_bonus = ITEMS[character['equipped_weapon']]['value']
    if character['equipped_armor']:
        armor_bonus = ITEMS[character['equipped_armor']]['value']

    print("\n📊 Stats:")
    for stat, value in character['stats'].items():    
        if stat == 'attack' and weapon_bonus > 0:
            print(f" - Attack: {value} (+{weapon_bonus})")
        elif stat == 'defense' and armor_bonus > 0:
            print(f" - Defense: {value} (+{armor_bonus})")
        else:
            print(f" - {stat.capitalize()}: {value}")

    print("="*40)


def save_character(character):
    with open("character.json", "w") as f:
        json.dump(character, f, indent=4)
    
    print("\nCharacter saved successfully!")

def load_character():
    if not os.path.exists("character.json"):
        print("\n❌ No saved character found!")
        return None
    
    with open("character.json", "r") as f:
        character = json.load(f)
    print("\n✅ Character loaded successfully!")
    display_character(character)
    return character

ENEMIES = {
    "goblin": {
        "name": "Goblin",
        "health": 30,
        "attack": 8,
        "exp": 50,
        "gold":20,
    },
    "wolf": {
        "name": "Wolf",
        "health": 25,
        "attack": 10,
        "exp": 40,
        "gold": 15
    },
    "orc": {
        "name": "Orc",
        "health": 50,
        "attack": 12,
        "exp": 60,
        "gold": 30
    }
}

def create_enemy(enemy_type):
    return ENEMIES[enemy_type].copy()

def combat(character, enemy):
    print(f"A wild {enemy['name']} appears!")

    while character['stats']['health'] > 0 and enemy['health'] > 0:
        print("\n" + "="*40)
        print("=== YOUR TURN ===")
        time.sleep(1)
        print("\n")
        print(f"{enemy['name']} HP : {enemy['health']}")
        print(f"Your HP: {character['stats']['health']}/{character['max_health']}")
        print("Press 1 to Attack")
        print("Press 2 to Use Item")
        print("Press 3 to Run Away")

        action = input("Enter 1-3: ").strip()
        while action not in ['1','2','3']:
            print("Invalid choice!")
            action = input("Enter 1-3: ").strip()
        # Attack
        base_attack = character['stats']['attack']
        weapon_bonus = 0
        if character['equipped_weapon']:
            weapon_bonus = ITEMS[character['equipped_weapon']]['value']
        total_attack = base_attack + weapon_bonus
        # Defense
        base_defense = character['stats']['defense']
        armor_bonus = 0
        if character['equipped_armor']:
            armor_bonus = ITEMS[character['equipped_armor']]['value']
        total_defense = base_defense + armor_bonus

        if action == '1':
            chance = random.randint(1,100)
            if chance <= 10:
                critical = int(total_attack * 1.5)
                enemy['health'] -= critical
                print(f"\nCritical hit! Dealt {critical} damage!")
                time.sleep(1)
            else:
                enemy['health'] -= total_attack
                print(f"\nYou attacked! Dealt {total_attack} damage!")
                time.sleep(1)

        elif action == '2':
            consumables = [item for item in character['inventory'] if ITEMS[item]['type'] == 'consumable' and character['inventory'][item] > 0]
            if not consumables:
                print("No items to use!")
                continue
            for i, item in enumerate(consumables, 1):
                qty = character['inventory'][item]
                print(f"{i}. {ITEMS[item]['name']} x{qty}")
            
            choice = input("Choose: ")
            idx = int(choice) - 1
            item_id = consumables[idx]

            if item_id == 'health_potion':
                character['stats']['health'] += ITEMS[item_id]['value']
                if character['stats']['health'] >= character['max_health']:
                    character['stats']['health'] = character['max_health']
                print(f"Restored {ITEMS[item_id]['value']} HP!")
            
            elif item_id == 'strength_potion':
                boost = ITEMS[item_id]['value']
                total_attack += boost
                print(f"Attack boosted by {boost} for this turn!")
                enemy['health'] -= total_attack
                print(f"You attacked with boosted power! Dealt {total_attack} damage!")
            
            character['inventory'][item_id] -= 1

        elif action == '3':
            print("You ran away!")
            break

        if enemy['health'] <= 0:
            print("You won!")
            exp_gained = enemy['exp']
            character['exp'] += exp_gained
            gold_gained = enemy['gold']
            character['gold'] += gold_gained
            print(f"Gained {exp_gained} exp.")
            print(f"Gained {gold_gained} gold. (Total: {character['gold']} gold.)")
            time.sleep(1.5)
            break

        time.sleep(1)
        print("\n" + "=" *40)
        print("=== ENEMY'S TURN ===")
        time.sleep(1)
        damage = enemy['attack']
        defense = total_defense * 0.5
        final_damage = max(0, damage - defense)
        character['stats']['health'] -= final_damage
        print(f"Ouch! The enemy dealt {final_damage} damage to you!")
        time.sleep(1)
        
        if character['stats']['health'] <= 0:
            print("You died! The enemy was too strong.")
            time.sleep(1.5)
            break
    check_level_up(character)

def shop(character):
    print("\n" + "="*40)
    print("\n=== THE HERO'S HAVEN SHOP ===")
    print("🌟 Consumables :")
    print(f"1. 🩸 Health potion. Cost {ITEMS['health_potion']['cost']}")
    print(f"2. 💪 Strength potion. Cost {ITEMS['strength_potion']['cost']}")
    print("⚔️ Weapons :")
    print(f"3. 🗡️ Iron sword. Cost {ITEMS['iron_sword']['cost']}")
    print(f"4. 💎 Diamond sword. Cost {ITEMS['diamond_sword']['cost']}")
    print("🛡️ Armors :")
    print(f"5. ⛉ Iron armor. Cost {ITEMS['iron_armor']['cost']}")
    print(f"6. ⛉⛉ Diamond armor. Cost {ITEMS['diamond_armor']['cost']}")
    print("\n7. Back")
    choice = input("Enter 1-7: ")
    while choice not in ['1','2','3','4','5','6','7']:
        print("Invalid choice!")
        choice = input("Enter 1-6: ")

    if choice == '7':
        return
        
    item_map = {
        '1': 'health_potion',
        '2': 'strength_potion',
        '3': 'iron_sword',
        '4': 'diamond_sword',
        '5': 'iron_armor',
        '6': 'diamond_armor'
    }

    item_id = item_map[choice]
    item = ITEMS[item_id]

    if character['gold'] >= item['cost']:
        character['gold'] -= item['cost']
        # Use .get() to avoid KeyError
        character['inventory'][item_id] = character['inventory'].get(item_id, 0) + 1
        print(f"\nBought {item['name']}!")
        print(f"Gold remaining: {character['gold']}")
    else:
        print(f"Not enough gold! Need {item['cost']}, current gold {character['gold']}")

def inn(character):
    cost = 10
    if character['gold'] >= cost:
        character['gold'] -= cost
        print("Sleeping ...")
        character['stats']['health'] = character['max_health']
        time.sleep(1)
        print("HP is fully restored!")
        print(f"Paid {cost}. Current gold: {character['gold']}")
    else:
        print(f"Not enough gold! Need {cost} gold. Only have {character['gold']} gold.")

def view_inventory(character):
    print("\n" + "="*40)
    print("=== INVENTORY ===")
    print(f"Gold : {character['gold']}")

    if not character['inventory']:
        print("Your inventory is empty!")
        return
    print("\nItems:")
    for item_id, quantity in character['inventory'].items():
        item_name = ITEMS[item_id]['name']
        print(f" - {item_name} x{quantity}")
    
    print("="*40)

def check_level_up(character):
    if character['exp'] >= 100:
        character['level'] += 1
        character['exp'] -= 100

        if character['class'] == 'warrior':
            character['stats']['attack'] += 3
            character['stats']['health'] += 10
            character['max_health'] += 10
        elif character['class'] == 'mage':
            character['stats']['attack'] += 5
            character['stats']['health'] += 8
            character['max_health'] += 8
        elif character['class'] == 'rogue':
            character['stats']['attack'] += 4
            character['stats']['health'] += 9
            character['max_health'] += 9
        
        print(f"Level up! You are now level {character['level']}")

def equipment_menu(character):
    print("\n=== EQUIPMENT ===")
    print("Currently Equipped:")
    
    if character['equipped_weapon']:
        weapon_name = ITEMS[character['equipped_weapon']]['name']
        value = ITEMS[character['equipped_weapon']]['value']
        print(f"Weapon : {weapon_name} (+{value} ATK)")
    else:
        print("Weapon: None")
    
    if character['equipped_armor']:
        armor_name = ITEMS[character['equipped_armor']]['name']
        value = ITEMS[character['equipped_armor']]['value']
        print(f"Armor : {armor_name} (+{value} DEF)")
    else:
        print("Armor: None")

    print("\nAvailable Weapons:")
    found = False
    for item_id in character['inventory']:
        item = ITEMS[item_id]
        if item['type'] == 'weapon':
            print(f"- {item['name']} (+{item['value']} ATK)")
            found = True
    if not found:
        print("None")

    print("\nAvailable Armor")
    found = False
    for item_id in character['inventory']:
        item = ITEMS[item_id]
        if item['type'] == 'armor':
            print(f"- {item['name']} (+{item['value']} DEF)")
            found = True
    if not found:
        print("None")
    print("\n1. Equip/Unequip Weapon")
    print("2. Equip/Unequip Armor")
    print("3. Back")

    choice = input("Enter 1-3: ")

    if choice == '1':
        weapons = [item for item in character['inventory'] if ITEMS[item]['type'] == 'weapon']
        if not weapons:
            print("No weapons to equip!")
            return
        for i, weapon in enumerate(weapons, 1):
            print(f"{i}. {ITEMS[weapon]['name']}")
        
        w_choice = input("Choose weapon (or 0 to unequip): ")
        if w_choice == '0':
            character['equipped_weapon'] = None
        else:
            idx = int(w_choice) - 1
            character['equipped_weapon'] = weapons[idx]
            print(f"Equipped {ITEMS[weapons[idx]]['name']}!")
    
    elif choice == '2':
        armors = [item for item in character['inventory'] if ITEMS[item]['type'] == 'armor']
        if not armors:
            print("No armors to equip!")
            return
        for i, armor in enumerate(armors, 1):
            print(f"{i}. {ITEMS[armor]['name']}")
        
        w_choice = input("Choose armor (or 0 to unequip): ")
        if w_choice == '0':
            character['equipped_armor'] = None
        else:
            idx = int(w_choice) - 1
            character['equipped_armor'] = armors[idx]
            print(f"Equipped {ITEMS[armors[idx]]['name']}!")
    
    elif choice == '3':
        return


def main():
    character = None
    while True:
        print("\n" + "="*40)
        print("⚔️ RPG CHARACTER MANAGER ⚔️")
        print("="*40)
        print("\n1. Create New Character")
        print("2. Load Character")
        print("3. Display Character")
        print("4. Enter combat")
        print("5. The Hero's Haven")
        print("6. Exit")

        choice = input("Enter 1-6: ").strip()

        if choice == '1':
            character = create_character()
            save_character(character)
        
        elif choice == '2':
            character = load_character()

        elif choice == '3':
            if character is not None:
                display_character(character)
            else:
                print("No character yet! Create or load a character first.")
        
        elif choice == '4':
            if character: # if character is not None
                enemy_type = random.choice(['goblin', 'wolf', 'orc'])
                enemy = create_enemy(enemy_type)
                combat(character, enemy)
                save_character(character)
            else:
                print("No character loaded! Create or load a character first.")
        
        elif choice == '5':
            print("\n" + "="*40)
            print("=== THE HERO'S HAVEN ===")
            print("Welcome, traveler!")
            print("\n1. Shop (Buy Items)")
            print("2. View Inventory")
            print("3. Equipment")
            print("4. Inn")
            print("5. Back to Main Menu")

            haven_choice = input("Enter 1-5: ")
            if haven_choice == '1':
                if character:
                    shop(character)
                    save_character(character)
                else:
                    print("No character loaded!")
            
            elif haven_choice == '2':
                if character:
                    view_inventory(character)
                else:
                    print("No character loaded!")
            
            elif haven_choice == '3':
                if character:
                    equipment_menu(character)
                    save_character(character)
                else:
                    print("No character loaded!")
            
            elif haven_choice == '4':
                if character:
                    inn(character)
                    save_character(character)
                else:
                    print("No character loaded!")
            
            elif haven_choice == '5':
                continue

        elif choice == '6':
            print("\n Thanks for playing! See you next time.")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
