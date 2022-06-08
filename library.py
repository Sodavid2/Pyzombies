import time as t
import copy as c

GAME_SPEED = 1.4


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
    inventory_capacity = 10
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
plank = Weapon("plank", 20, 26, 1.6, 1.04, False, 0, 12, 0.8, 13)
plank_nails = Weapon("plank with nails", 26, 32, 1.6, 1.02, False, 0, 14, 1.2, 13)
table_leg = Weapon("table leg", 22, 28, 2.0, 0.94, False, 0, 14, 1.2, 12)
bat = Weapon("baseball bat", 34, 42, 1.6, 0.92, False, 0, 18, 2.5, 16)
bat_nails = Weapon("baseball bat with nails", 42, 52, 1.6, 0.9, False, 0, 20, 3, 16)
pipe = Weapon("iron pipe", 26, 34, 1.4, 0.92, False, 0, 16, 1.6, 16)
crowbar = Weapon("crowbar", 32, 38, 2.0, 0.94, False, 0, 18, 2, 20)
hammer = Weapon("hammer", 28, 36, 1.2, 1.04, False, 0, 20, 1.4, 10)
large_hammer = Weapon("large hammer", 44, 56, 1.6, 0.9, None, 0, 30, 5, 14)
pocket_knife = Weapon("pocket knife", 28, 34, 1.2, 1.1, False, 0, 12, 0.3, 10)
knife = Weapon("knife", 34, 42, 1.3, 1.02, False, 0, 16, 0.4, 12)
machete = Weapon("machete", 52, 60, 1.4, 0.94, False, 0, 22, 1.2, 14)
axe = Weapon("axe", 42, 52, 1.6, 0.9, False, 0, 24, 3, 14)
fire_axe = Weapon("firefighter axe", 56, 64, 1.8, 0.92, False, 0, 28, 4, 16)

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


# (name, health, armor, speed, accuracy, agility, damage_min, damage_max, range, effects, probability)
rotten_zombie = Enemy("rotten zombie", 80, 0, 0.8, 0.65, 0.95, 6, 10, 1, [], 0.0)
zombie = Enemy("zombie", 100, 0, 1, 0.7, 1.0, 8, 12, 1, ["bleeding"], 0.3)
runner = Enemy("runner", 80, 0, 1.3, 0.75, 1.1, 10, 14, 1, ["bleeding", "wounded arm"], 0.4)
sprinter = Enemy("sprinter", 90, 5, 1.6, 0.75, 1.2, 12, 16, 1, ["bleeding", "wounded arm"], 0.5)
big_zombie = Enemy("big zombie", 140, 5, 0.9, 0.7, 0.95, 12, 16, 1, ["bleeding", "wounded leg"], 0.4)
armored_zombie = Enemy("armored zombie", 120, 10, 0.8, 0.7, 0.9, 8, 12, 1, ["bleeding"], 0.3)
giant_zombie = Enemy("giant zombie", 200, 10, 0.7, 0.8, 0.8, 14, 18, 1.5, ["wounded leg", "wounded arm"], 0.6)
slender_zombie = Enemy("slender zombie", 120, 5, 1.2, 0.8, 1, 8, 12, 2, ["bleeding", "wounded leg"], 0.6)
spitter = Enemy("spitter", 70, 0, 0.8, 0.6, 0.9, 6, 10, 5, [], 0.0)
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
            t.sleep(GAME_SPEED)
            return True
        else:
            print("wrong ammo type")
            t.sleep(GAME_SPEED)
            return False
    else:
        return False


def get_effect(effect, amout):
    for i in range(amout):
        P.effects.append(effect)
    print("you got effect: {} x {}".format(effect, amout))
    t.sleep(GAME_SPEED)
    return True


def heal_effect(effect, amout):  # removes specific amout of specific effect type
    for i in range(amout):
        if effect in P.effects:
            del P.effects[P.effects.index(effect)]
    print(effect, "removed")
    t.sleep(GAME_SPEED)
    return True


def eat(amout, item):
    P.hunger += amout
    if P.hunger > P.max_hunger:
        P.hunger = P.max_hunger
    print("you ate", item)
    t.sleep(GAME_SPEED)
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
    before = P.health
    P.health += 30
    if P.health > P.max_health:
        P.health = P.max_health
    print("you got {} HP".format(P.health - before))
    return True


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
    t.sleep(GAME_SPEED * 2)
    return True


red_pill = Item("red pill", use_red_pill, 0.1)


def use_blue_pill():
    P.max_stamina += 20
    print("maximum stamina increased by 20")
    t.sleep(GAME_SPEED * 2)
    return True


blue_pill = Item("blue pill", use_blue_pill, 0.1)


def use_green_pill():
    P.stamina_refill += 6
    print("stamina refill increased by 6")
    t.sleep(GAME_SPEED * 2)
    return True


green_pill = Item("green pill", use_green_pill, 0.1)


# world ----------------------------------------------------------------------------------------------------------------

class World:
    time = 360
    location = None


class Building:
    def __init__(self, name, danger, loot, loot_weight, loot_amount):
        self.type = "building"
        self.name = name
        self.danger = danger
        self.loot = loot
        self.loot_weight = loot_weight
        self.loot_amount = loot_amount


small_house_loot = [bread, apple, medkit, plank, table_leg, pocket_knife]
small_house_weight = [5, 10, 5, 5, 5, 5]
small_house = Building("small house", 3, small_house_loot, small_house_weight, 5)

house_loot = [hamburger, bread, medkit, plank_nails, bat, axe, handgun, ammo_7mm]
house_weight = [5, 10, 10, 5, 5, 5, 5, 10]
house = Building("house", 4, house_loot, house_weight, 6)

pharmacy_loot = [medkit, bandage, morphine, revolver, knife, red_pill, blue_pill, green_pill]
pharmacy_weight = [10, 10, 10, 5, 5, 5, 5, 5]
pharmacy = Building("pharmacy", 3, pharmacy_loot, pharmacy_weight, 5)

hospital_loot = [medkit, bandage, morphine, red_pill, blue_pill, green_pill, machete]
hospital_weight = [10, 10, 10, 5, 5, 5, 5]
hospital = Building("hospital", 5, hospital_loot, hospital_weight, 7)

grocery_loot = [meat, hamburger, bread, apple, pipe, knife]
grocery_weight = [10, 10, 10, 10, 5, 5]
grocery = Building("grocery", 4, grocery_loot, grocery_weight, 6)

utility_store_loot = [bat_nails, crowbar, hammer, plank_nails, fire_axe, bow, arrows]
utility_store_weight = [10, 10, 10, 10, 5, 10, 20]
utility_store = Building("utility store", 4, utility_store_loot, utility_store_weight, 5)

police_station_loot = [handgun, rifle, shotgun, ammo_7mm, ammo_shotgun, medkit, MRE_pack]
police_station_weight = [5, 5, 5, 15, 10, 10, 10]
police_station = Building("police station", 5, police_station_loot, police_station_weight, 6)

abandoned_house_loot = [apple, bat, axe, bow, arrows]
abandoned_house_weight = [10, 10, 5, 10, 15]
abandoned_house = Building("abandoned house", 3, abandoned_house_loot, abandoned_house_weight, 4)

meadow_loot = [berries, apple, pocket_knife, table_leg]
meadow_weight = [10, 10, 5, 5]
meadow = Building("meadow", 2, meadow_loot, meadow_weight, 3)


class Location:
    def __init__(self, name, size, structures, structure_weights, enemies, enemy_weights):
        self.type = "location"
        self.name = name
        self.size = size
        self.structures = structures
        self.structure_weights = structure_weights
        self.enemies = enemies
        self.enemy_weights = enemy_weights


forest_structures = [meadow, abandoned_house, small_house]
forest_structures_weights = [10, 5, 5]
forest_enemies = [zombie, rotten_zombie, runner, sprinter, slender_zombie]
forest_enemy_weights = [20, 10, 10, 5, 5]
forest = Location("forest", 8, forest_structures, forest_structures_weights, forest_enemies, forest_enemy_weights)

village_structures = [small_house, house, pharmacy, grocery, utility_store]
village_structures_weights = [10, 20, 10, 10, 10]
village_enemies = [zombie, rotten_zombie, big_zombie, armored_zombie, spitter]
village_enemy_weights = [20, 10, 5, 5, 10]
village = Location("village", 12, village_structures, village_structures_weights, village_enemies, village_enemy_weights)

city_structures = [house, grocery, utility_store, hospital, police_station]
city_structures_weights = [20, 10, 10, 10, 10]
city_enemies = [zombie, spitter, big_zombie, armored_zombie, sprinter, giant_zombie, slender_zombie]
city_enemy_weights = [20, 20, 5, 5, 5, 5, 5]
city = Location("city", 16, city_structures, city_structures_weights, city_enemies, city_enemy_weights)


class World_type:
    def __init__(self, name, locations, weights):
        self.type = "world"
        self.name = name
        self.locations = locations
        self.weights = weights


test_world_locations = [forest, village, city]
test_world_weights = [10, 6, 4]
test_world = World_type("test world", test_world_locations, test_world_weights)


class Statistics:  # incomplete
    enemies_killed = 0
    items_found = 0
    cheats = "no"
