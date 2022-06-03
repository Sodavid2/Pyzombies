import time as t
import copy as c

game_speed = 1.4


def myinput(possible):
    character = None
    first = True
    while character not in possible:
        if not first:
            print("enter:", possible)
        character = input("-> ")
        first = False
        try:
            character = int(character)
        except:
            pass
    return character


def player_weapons():
    print("  weapons:")
    x = 1
    for weapon in P.weapons:
        if weapon.name == "fists":
            print("   {}. fists".format(x))
        elif not weapon.durability:
            print("   {}. {} - {}/{} ({})".format(x, weapon.name, weapon.ammo, weapon.max_ammo, weapon.ammo_type))
        else:
            print("   {}. {} - {}/{} durability".format(x, weapon.name, weapon.durability, weapon.max_durability))
        x += 1


# player ---------------------------------------------------------------------------------------------------------------


class P:  # player stats
    name = "player"
    def_max_health = 100  # unused
    max_health = 100
    health = 100
    max_hunger = 100
    hunger = 100
    hunger_modifier = 0.4
    def_max_stamina = 100  # unused
    max_stamina = 100
    stamina = 100
    def_stamina_refill = 30
    stamina_refill = 30
    def_strength = 1.0
    strength = 1.0
    def_accuracy = 1.0
    accuracy = 1.0
    def_agility = 1.0
    agility = 1.0
    defense = 0
    armor = 0
    inventory_capacity = 8
    inventory_used = 0
    inventory = []
    weapons = [None, None, None]
    effects = []
    default_effect_time = {"weak": 3, "wounded leg": 60, "wounded arm": 60, "bleeding": 5, "starving": 1,
                           "regeneration": 5}
    effect_time = c.deepcopy(default_effect_time)


# weapons --------------------------------------------------------------------------------------------------------------

class Weapon:  # creates weapons
    def __init__(self, name, damage_min, damage_max, range, accuracy,
                 ammo_type, max_ammo, stamina_cost, weight, durability):
        self.type = "weapon"
        self.name = name
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.range = range
        self.accuracy = accuracy
        self.ammo_type = ammo_type
        self.max_ammo = max_ammo
        self.stamina_cost = stamina_cost
        self.weight = weight
        self.max_durability = durability
        self.durability = durability
        self.ammo = False
        if ammo_type:
            self.ammo = 0


# (name, damage_min, damage_max, range, accuracy, ammo_type, max_ammo, stamina_cost, weight, durability)
fists = Weapon("fists", 18, 22, 1, 1.0, False, 0, 10, 0, False)
plank = Weapon("plank", 20, 26, 1.4, 1.04, False, 0, 12, 0.8, 12)
plank_nails = Weapon("plank with nails", 26, 32, 1.4, 1.02, False, 0, 14, 1.2, 16)
table_leg = Weapon("table leg", 22, 28, 1.8, 0.94, False, 0, 14, 1.2, 14)
bat = Weapon("baseball bat", 34, 42, 1.6, 0.92, False, 0, 18, 2.5, 20)
bat_nails = Weapon("baseball bat with nails", 42, 52, 1.6, 0.9, False, 0, 20, 3, 24)
pipe = Weapon("iron pipe", 26, 34, 1.4, 0.92, False, 0, 16, 1.6, 18)
crowbar = Weapon("crowbar", 32, 38, 1.8, 0.94, False, 0, 18, 2, 22)
hammer = Weapon("hammer", 28, 36, 1.2, 1.04, False, 0, 20, 1.4, 14)
large_hammer = Weapon("large hammer", 44, 56, 1.4, 0.9, None, 0, 30, 5, 18)
pocket_knife = Weapon("pocket knife", 28, 34, 1.2, 1.1, False, 0, 12, 0.3, 10)
knife = Weapon("knife", 34, 42, 1.2, 1.02, False, 0, 16, 0.4, 12)
machete = Weapon("machete", 52, 60, 1.4, 0.94, False, 0, 22, 1.2, 16)
axe = Weapon("axe", 42, 52, 1.6, 0.9, False, 0, 24, 3, 20)
fire_axe = Weapon("firefighter axe", 56, 64, 1.8, 0.92, False, 0, 28, 4, 24)

bow = Weapon("bow", 24, 32, 10, 1.0, "arrows", 10, 10, 2, False)
handgun = Weapon("handgun", 32, 42, 20, 1.04, "7mm ammo", 8, False, 1.2, False)
revolver = Weapon("revolver", 38, 46, 10, 1.0, "7mm ammo", 6, False, 1.4, False)
rifle = Weapon("rifle", 48, 56, 30, 1.08, "7mm ammo", 5, False, 2.6, False)
shotgun = Weapon("shotgun", 82, 102, 4, 1.02, "shotgun shells", 4, False, 3.2, False)


# enemies --------------------------------------------------------------------------------------------------------------


class Enemy:  # creates enemies
    def __init__(self, name, health, armor, speed, accuracy, agility, damage_min, damage_max, range, effects,
                 probability):
        self.type = "enemy"
        self.name = name
        self.max_health = health
        self.health = health
        self.armor = armor
        self.speed = speed
        self.distance = 0
        self.accuracy = accuracy
        self.agility = agility
        self.strength = 1.0
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.range = range
        self.effects = effects
        self.probability = probability


def create_enemy(enemy):  # returns enemy
    e = enemy
    return Enemy(e.name, e.health, e.armor, e.speed, e.accuracy, e.agility, e.damage_min, e.damage_max, e.range,
                 e.effects, e.probability)


# (name, health, armor, speed, accuracy, agility, damage_min, damage_max, range, effects, probability)
rotten_zombie = Enemy("rotten zombie", 80, 0, 0.8, 0.65, 0.95, 6, 10, 1, [], 0.0)
zombie = Enemy("zombie", 100, 0, 1, 0.7, 1.0, 8, 12, 1, ["bleeding"], 0.4)
runner = Enemy("runner", 80, 0, 1.3, 0.75, 1.1, 10, 14, 1, ["bleeding", "wounded arm"], 0.5)
sprinter = Enemy("sprinter", 90, 10, 1.6, 0.75, 1.2, 14, 18, 1, ["bleeding", "wounded arm"], 0.6)
big_zombie = Enemy("big zombie", 140, 10, 0.9, 0.7, 0.95, 12, 16, 1, ["bleeding", "wounded arm"], 0.5)
armored_zombie = Enemy("armored zombie", 120, 15, 0.8, 0.7, 0.9, 8, 12, 1, ["bleeding"], 0.4)
giant_zombie = Enemy("giant zombie", 200, 10, 0.7, 0.8, 0.8, 14, 20, 1.5, ["wounded leg", "wounded arm"], 0.7)
slender_zombie = Enemy("slender zombie", 120, 5, 1.2, 0.8, 1, 10, 14, 2, ["bleeding", "wounded leg"], 0.8)
spitter = Enemy("spitter", 70, 0, 0.8, 0.5, 0.9, 6, 10, 5, [], 0.0)
# enemy group ----------------------------------------------------------------------------------------------------------
random = [rotten_zombie, zombie, runner, sprinter, big_zombie, armored_zombie, giant_zombie, slender_zombie]


# items ----------------------------------------------------------------------------------------------------------------


def load_ammo(type):
    player_weapons()
    print("select weapon:")
    input = myinput([0, 1, 2, 3])
    if input != 0:
        weapon = P.weapons[input - 1]
        if weapon.ammo_type == type:
            weapon.ammo = weapon.max_ammo
            print(weapon.name, "reloaded")
            t.sleep(game_speed)
            return True
        else:
            print("wrong ammo type")
            t.sleep(game_speed)
            return False
    else:
        return False


def get_effect(effect, amout):
    for i in range(amout):
        P.effects.append(effect)
    print("you got effect: {} x {}".format(effect, amout))
    t.sleep(game_speed)
    return True


def heal_effect(effect, amout):  # removes specific amout of specific effect type
    for i in range(amout):
        if effect in P.effects:
            del P.effects[P.effects.index(effect)]
    print(effect, "removed")
    t.sleep(game_speed)
    return True


def eat(amout, item):
    P.hunger += amout
    if P.hunger > P.max_hunger:
        P.hunger = P.max_hunger
    print("you ate", item)
    t.sleep(game_speed)
    return True


class Item:
    def __init__(self, name, action, weight):
        self.type = "item"
        self.name = name
        self.action = action
        self.weight = weight


def use_medkit():
    return get_effect("regeneration", 3)


medkit = Item("medkit", use_medkit, 0.5)


def use_bandage():
    return heal_effect("bleeding", 3)


bandage = Item("bandage", use_bandage, 0.2)


def use_morphine():
    return get_effect("regeneration", 2)


morphine = Item("morphine", use_morphine, 0.2)


def use_ammo_shotgun():
    return load_ammo("shotgun shells")


ammo_shotgun = Item("shotgun shells", use_ammo_shotgun, 0.3)


def use_ammo_7mm():
    return load_ammo("7mm ammo")


ammo_7mm = Item("7mm ammo", use_ammo_7mm, 0.2)


def use_arrows():
    return load_ammo("arrows")


arrows = Item("arrows", use_arrows, 0.4)


def use_berries():
    return eat(10, "berries")


berries = Item("berries", use_berries, 0.1)


def use_apple():
    return eat(16, "apple")


apple = Item("apple", use_apple, 0.2)


def use_bread():
    return eat(20, "bread")


bread = Item("bread", use_bread, 0.3)


def use_hamburger():
    return eat(26, "hamburger")


hamburger = Item("hamburger", use_hamburger, 0.3)


def use_meat():
    return eat(30, "meat")


meat = Item("meat", use_meat, 0.4)


def use_MRE_pack():
    return eat(50, "MRE pack")


MRE_pack = Item("MRE pack", use_MRE_pack, 0.5)


def use_red_pill():
    P.max_health += 20
    P.health += 20
    print("maximum health increased by 20")
    t.sleep(game_speed * 2)
    return True


red_pill = Item("red pill", use_red_pill, 0.1)


def use_blue_pill():
    P.max_stamina += 20
    print("maximum stamina increased by 20")
    t.sleep(game_speed * 2)
    return True


blue_pill = Item("blue pill", use_blue_pill, 0.1)


def use_green_pill():
    P.stamina_refill += 6
    print("stamina refill increased by 6")
    t.sleep(game_speed * 2)
    return True


green_pill = Item("green pill", use_green_pill, 0.1)


# world ----------------------------------------------------------------------------------------------------------------

class World:
    time = 360
    location = None


class Building:
    def __init__(self, name, danger, loot, loot_weight, size):
        self.type = "building"
        self.name = name
        self.danger = danger
        self.loot = loot
        self.loot_weight = loot_weight
        self.size = size


house_loot = [apple, medkit, pipe, handgun, ammo_7mm]
house_weight = (10, 6, 6, 4, 6)
house = Building("house", 4, house_loot, house_weight, 4)

pharmacy_loot = [medkit, bandage]
pharmacy_weight = (10, 6)
pharmacy = Building("pharmacy", 3, pharmacy_loot, pharmacy_weight, 3)

shop_loot = [apple, pipe, axe, large_hammer, bow, arrows]
shop_weight = (10, 10, 4, 4, 4, 10)
shop = Building("shop", 5, shop_loot, shop_weight, 4)

abondomed_house_loot = [pipe, axe, bow, arrows, handgun]
abondomed_house_weight = (4, 2, 2, 4, 2)
abondomed_house = Building("abondomed house", 3, abondomed_house_loot, abondomed_house_weight, 3)

meadow_loot = [apple, table_leg]
meadow_weight = (10, 10)
meadow = Building("meadow", 2, meadow_loot, meadow_weight, 2)


class Location:
    def __init__(self, name, size, structures, structure_weights):
        self.type = "location"
        self.name = name
        self.size = size
        self.structures = structures
        self.structure_weights = structure_weights


town_buildings = [house, pharmacy, shop]
town_weight = (10, 4, 4)
town = Location("town", 5, town_buildings, town_weight)

forest_buildings = [meadow, abondomed_house, house]
forest_weight = [10, 4, 2]
forest = Location("forest", 3, forest_buildings, forest_weight)


class Statistics:  # incomplete
    enemies_killed = 0
