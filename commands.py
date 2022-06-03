from library import *
import random as r
import os

debug_mode = True


# inventory ------------------------------------------------------------------------------------------------------------


def update_inventory():
    item_weight = 0
    for item in P.inventory:
        item_weight += item.weight
    P.inventory_used = item_weight


def get_item(item):
    if item.type == "item":
        P.inventory.append(item)
    elif item.type == "weapon":
        P.inventory.append(c.deepcopy(item))
    else:
        print(item.name, "can't be added to inventory")
        t.sleep(game_speed)
    print(item.name, "picked up")
    t.sleep(game_speed)
    update_inventory()


def open_inventory(battle=False):
    while True:
        if not battle:
            player_info(inventory=True)
        else:
            player_battle_info()
            print("inventory {}/{}Kg:".format(round(P.inventory_used,1), P.inventory_capacity))
            item_list(P.inventory)
        item = None
        item_name = input("item: ")
        if item_name == "0":
            return
        else:
            for object in P.inventory:
                if object.name == item_name:
                    item = object
            if item in P.inventory:
                print("1 -drop")
                print("2 -use/equip")
                action = myinput([0, 1, 2])
                if action == 1:
                    P.inventory.remove(item)
                    update_inventory()
                elif action == 2:
                    if item.type == "item":
                        used = item.action()
                        if used:
                            P.inventory.remove(item)
                        update_inventory()
                    if item.type == "weapon":
                        print("equip to slot:")
                        print("  1)", P.weapons[0].name)
                        print("  2)", P.weapons[1].name)
                        print("  3)", P.weapons[2].name)
                        slot = myinput([0, 1, 2, 3])
                        if slot != 0:
                            previous = P.weapons[slot - 1]
                            P.weapons[slot - 1] = item
                            if previous != fists:
                                P.inventory.append(previous)
                            print(item.name, "equipped")
                            t.sleep(game_speed)
                            P.inventory.remove(item)
                            update_inventory()
            else:
                print("item not found")
                t.sleep(game_speed)


# world ----------------------------------------------------------------------------------------------------------------


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def game_setup():
    for i in range(3):
        P.weapons[i] = fists
    P.name = input("your name: ")
    clear_console()


def pass_time(amout=1):
    for i in range(amout):
        World.time += 1
        update_effects()
        P.hunger -= P.hunger_modifier
        P.health += 0.5
        if P.hunger < 0:
            P.effects.append("starving")
            P.hunger = 0
        if P.health > P.max_health:
            P.health = P.max_health
        inspect_health()
    t.sleep(game_speed)


# info -----------------------------------------------------------------------------------------------------------------


def bar(actual, maximum):
    max_lenght = 500
    ratio = 5.0
    if maximum > max_lenght:
        ratio = ratio * (maximum / max_lenght)
    maximum = round(maximum / ratio)
    actual = round(actual / ratio)
    bar = ""
    for i in range(actual):
        bar += "■"
    for i in range(maximum - actual):
        bar += "□"
    return bar


def digital_time():
    day = World.time // 1440
    hour = (World.time % 1440) // 60
    minute = World.time % 60
    hour = str(hour)
    if len(hour) < 2:
        hour = "0" + hour
    minute = str(minute)
    if len(minute) < 2:
        minute = "0" + minute
    print("day {} - {}:{}".format(day, hour, minute))


def enemy_info(enemy):
    print(enemy.name, "HP ({}):".format(round(enemy.health)), bar(enemy.health, enemy.max_health))
    print("  distance:", enemy.distance, "m")


def item_list(inventory):
    counted = []
    for item in inventory:
        if item.type == "item":
            if item not in counted:
                print("  {} x {} ({}Kg)".format(item.name, inventory.count(item), item.weight * inventory.count(item)))
                counted.append(item)
        elif item.type == "weapon":
            if not item.durability:
                print("  {} - {}/{} ({}, {}Kg)".format(item.name, item.ammo, item.max_ammo, item.ammo_type, item.weight))
            else:
                print("  {} - {}/{} durability ({}Kg)".format(item.name, item.durability, item.max_durability, item.weight))


def effects_info():
    effects = ""
    counted = []
    for effect in P.effects:
        if effect not in counted:
            effects = effects + str("{} x {}, ".format(str(effect), P.effects.count(effect)))
            counted.append(effect)
    print("  effects:", effects[:-2])


def player_info(inventory=False):
    clear_console()
    digital_time()
    print(P.name, "HP ({}):".format(round(P.health)), bar(P.health, P.max_health))
    print("  hunger ({}):".format(round(P.hunger)), bar(P.hunger, P.max_hunger))
    print("  {}-str {}-acc {}-agi {}-defense".format(round(P.strength, 2), round(P.accuracy, 2), round(P.agility, 2),
                                                     P.defense))
    print("  stamina: {} ({} refill)".format(P.max_stamina, P.stamina_refill))
    print("  weapons: {}, {}, {}".format(P.weapons[0].name, P.weapons[1].name, P.weapons[2].name))
    effects_info()
    if not inventory:
        print("  inventory {}/{}Kg".format(round(P.inventory_used, 2), P.inventory_capacity))
    else:
        print("  inventory {}/{}Kg:".format(round(P.inventory_used, 2), P.inventory_capacity))
        item_list(P.inventory)


def player_battle_info():
    clear_console()
    print(P.name, "HP ({}):".format(round(P.health)), bar(P.health, P.max_health))
    print("  stamina ({}):".format(round(P.stamina)), bar(P.stamina, P.max_stamina))
    effects_info()


# effects --------------------------------------------------------------------------------------------------------------


def inspect_health():
    if P.health <= 0:
        print("you died")
        t.sleep(game_speed)
        print("enemies killed:", Statistics.enemies_killed)
        input()
        exit()


def update_effects():
    P.strength = P.def_strength
    P.accuracy = P.def_accuracy
    P.agility = P.def_agility
    bleeding_amout = 0
    if "regeneration" in P.effects:
        P.health += 2
        if P.health > P.max_health:
            P.health = P.max_health
    for effect in P.effects:
        if effect == "weak":
            P.strength -= 0.1
        elif effect == "wounded leg":
            P.agility -= 0.1
        elif effect == "wounded arm":
            P.accuracy -= 0.1
        elif effect == "bleeding":
            bleeding_amout += 1
        elif effect == "starving":
            P.health -= 4
            inspect_health()
    if bleeding_amout > 0:
        bleeding_damage = round(1.5 + (bleeding_amout * 0.5), 1)
        P.health -= bleeding_damage
        print("you take {} damage from bleeding".format(bleeding_damage))
        inspect_health()
        t.sleep(game_speed / 2)
    applyed = []
    for effect in P.effects:
        if effect not in applyed:
            P.effect_time[effect] -= 1
            applyed.append(effect)
            if P.effect_time[effect] <= 0:
                if effect not in ["starving"]:
                    print("effect", effect, "stopped")
                    t.sleep(game_speed / 2)
                P.effects.remove(effect)
                P.effect_time[effect] = P.default_effect_time[effect]


# fight ----------------------------------------------------------------------------------------------------------------


def enemy_attack(enemy):  # attack entyty with weapon
    accuracy = (enemy.accuracy / P.agility) - (enemy.distance / 30)
    print(enemy.name, "hit chance:", round(accuracy * 100), "%")
    t.sleep(game_speed)
    if accuracy > r.random():
        raw_damage = r.randint(enemy.damage_min, enemy.damage_max)
        damage = (raw_damage * enemy.strength) - (P.defense + P.armor)
        if P.armor >= 1:
            P.armor -= 1
        if damage < 0:
            damage = 0
        P.health -= damage
        print("{} inflicts {} {} DMG (blocked {})".format(enemy.name, P.name, round(damage),
                                                       round((raw_damage * enemy.strength) - damage)))
        inspect_health()
        t.sleep(game_speed)
        if damage > 0:
            if enemy.probability > r.random():
                effect = r.choice(enemy.effects)
                print("you got effect:", effect)
                P.effects.append(effect)
                t.sleep(game_speed)
    else:
        print(enemy.name, "missed")
        t.sleep(game_speed)


def player_attack(enemy, weapon):
    if weapon.ammo_type:
        if weapon.ammo > 0:
            weapon.ammo -= 1
        else:
            print("no ammo")
            t.sleep(game_speed)
            return 0
    if weapon.stamina_cost:
        if P.stamina >= weapon.stamina_cost:
            P.stamina -= weapon.stamina_cost
        else:
            print("not enough stamina")
            t.sleep(game_speed)
            return 0
    accuracy = (((weapon.accuracy * P.accuracy) / enemy.agility) - enemy.distance / 30)
    print("hit chance:", round(accuracy * 100), "%")
    t.sleep(game_speed)
    if accuracy > r.random():
        raw_damage = r.randint(weapon.damage_min, weapon.damage_max)
        strength = P.strength
        if weapon.ammo_type:  # ranged weapons ignore strength
            strength = 1.0
        damage = (raw_damage * strength) - enemy.armor
        if damage < 0:
            damage = 0
        enemy.health -= damage
        print("{} inflicts {} {} DMG (blocked {})".format(P.name, enemy.name, round(damage),
                                                       round((raw_damage * strength) - damage)))
        t.sleep(game_speed)
        if weapon.durability:
            weapon.durability -= 1
            if weapon.durability <= 0:
                P.weapons[P.weapons.index(weapon)] = fists
                print(weapon.name, "is broken")
                t.sleep(game_speed)
        return -1
    else:
        print(P.name, "missed")
        t.sleep(game_speed)
        return -1


def fight(enemy_count=1, enemy_pool=random, random_enemies=True):
    P.stamina = P.max_stamina
    if enemy_count < 1:
        enemy_count = 1
    enemies = []
    if random_enemies:
        for i in range(enemy_count):
            enemies.append(c.deepcopy(r.choice(enemy_pool)))
            enemies[i].distance = r.randint(20 + (i * 5), 30 + (i * 10)) / 10
    else:
        for i in range(len(enemy_pool)):
            enemies.append(c.deepcopy(enemy_pool[i]))
            enemies[i].distance = r.randint(20, 30 + (i * 10)) / 10

    def update_screen():
        player_battle_info()
        player_weapons()
        print("  actions:", actions)
        for enemy in enemies:
            print("{}.----------------------------------------".format(enemies.index(enemy) + 1))
            enemy_info(enemy)
        print()

    while len(enemies) > 0:
        pass_time()
        P.armor = 0
        actions = 3
        while actions > 0:
            update_screen()
            print("select action")
            inp = myinput(["", 0, 1, 2, 3, "+", "cheat"])
            if inp == "cheat":
                enemies = []
                return
            elif inp == "+":
                open_inventory(battle=True)
                actions -= 1
            elif inp == "":  # rest
                P.stamina += P.stamina_refill * actions
                if P.stamina > P.max_stamina:
                    P.stamina = P.max_stamina
                actions = 0
                print("you rest")
                t.sleep(game_speed)
            elif inp == 0:  # block
                P.armor += 4*actions
                actions = 0
                print("you prepare to defend")
                t.sleep(game_speed)
            else:  # attack
                weapon = P.weapons[int(inp) - 1]
                if len(enemies) == 1:  # if there is 1 enemy chose him
                    enemy = enemies[0]
                else:  # else let player chose
                    print("select enemy")
                    enemy = myinput([x for x in range(1, len(enemies) + 1)])
                    enemy = enemies[enemy - 1]
                if weapon.range >= enemy.distance:  # if chosen enemy is in range attack him
                    actions += player_attack(enemy, weapon)
                    for enemy in enemies:  # if enemy health is less than 1 delete him from enemy list
                        if enemy.health < 1:
                            print(enemy.name, "died")
                            t.sleep(game_speed)
                            enemies.remove(enemy)
                            Statistics.enemies_killed += 1
                            if len(enemies) <= 0:
                                print("all enemies died")
                                t.sleep(game_speed)
                                input("press enter to continue ")
                                return ()
                else:  # else inform player
                    print(enemy.name, "not in range ({}m)".format(weapon.range))
                    t.sleep(game_speed)
        print("zombie turn")
        t.sleep(game_speed)
        update_screen()
        for enemy in enemies:  # for all enemies
            if enemy.distance > 0:  # come closer
                enemy.distance -= enemy.speed
                enemy.distance = round(enemy.distance, 2)
                if enemy.distance < 0:
                    enemy.distance = 0
        update_screen()
        for enemy in enemies:
            if enemy.distance <= enemy.range:  # if in range attack player
                enemy_attack(enemy)
            else:
                print(enemy.name, "can't reach")
                t.sleep(game_speed/2)
        t.sleep(game_speed/2)
