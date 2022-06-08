from commands import *

start_time = World.time
infection_amount = 1
TRAVEL_OPTIONS = 5
clear_console()

game_setup()
location = world_type.locations[0]
P.weapons[0] = c.deepcopy(pipe)
print("You should avoid dangerous locations (city) until you get better equipment.")
t.sleep(GAME_SPEED * 2)

while True:
    print("you arrived at", location.name)
    t.sleep(GAME_SPEED)
    stay = True
    travel_options = r.choices(world_type.locations, world_type.weights, k=TRAVEL_OPTIONS)
    travel_distances = []
    for i in range(len(travel_options)):
        travel_distances.append(r.randint(3, 5 + i))
    buildings = r.choices(location.structures, location.structure_weights, k=location.size)
    while stay:
        player_info()
        print("1 -inventory")
        print("2 -search for buildings")
        print("3 -travel")
        print("enter to rest")
        action = myinput([1, 2, 3, "", "cheat"])
        if action == 1:  # inventory
            open_inventory()
        elif action == 2:  # search for building
            if round(P.inventory_used) <= P.inventory_capacity:
                if len(buildings) <= 0:
                    print("you explored everything")
                    t.sleep(GAME_SPEED)
                else:
                    pass_time(10)
                    if (len(buildings) / location.size) > r.random():
                        building = r.choice(buildings)
                        buildings.remove(building)
                        print("you found", building.name)
                        t.sleep(GAME_SPEED)
                        infection_amount = 1 + ((World.time - start_time) / 1140)  # + 1 evolution for 1 day
                        enemy_count = r.randint(round(building.danger * 0.5 * infection_amount),
                                                round(building.danger * infection_amount))
                        print("you can see {} enemies".format(enemy_count))
                        t.sleep(GAME_SPEED)
                        print("0 -go away")
                        print("1 -go inside")
                        choice = myinput([0, 1])
                        if choice == 1:
                            fight(enemy_count=enemy_count, location=location)
                            loot = r.choices(building.loot, building.loot_weight,
                                             k=r.randint(round(building.loot_amount * 0.7), building.loot_amount))
                            clear_console()
                            print("you search the building")
                            t.sleep(GAME_SPEED)
                            for item in loot:
                                get_item(item)
                    else:
                        print("you didn't find anything")
                        t.sleep(GAME_SPEED)
            else:
                print("you carry too much items")
                t.sleep(GAME_SPEED)
        elif action == 3:  # travel
            if P.inventory_used <= P.inventory_capacity:
                print("you can travel to:")
                for i in range(len(travel_options)):
                    print("  {}) {} - {}km".format(i + 1, travel_options[i].name, travel_distances[i]))
                selected = myinput([x for x in range(len(travel_options) + 1)])
                if selected != 0:
                    hunger_cost = travel_distances[selected - 1] * 20 * P.hunger_modifier
                    travel = 1
                    if hunger_cost > P.hunger:
                        print("you don't have enough hunger")
                        print("0 -stay")
                        print("1 -continue")
                        travel = myinput([0, 1])
                    if travel == 1:
                        print("you travel to", travel_options[selected - 1].name)
                        stay = False
                        time = World.time
                        pass_time(round(travel_distances[selected - 1] * 20 / P.agility))
                        print("you travelled for {} minutes".format(World.time - time))
                        t.sleep(GAME_SPEED)
                        location = travel_options[selected - 1]
            else:
                print("you carry too many items")
                t.sleep(GAME_SPEED)
        elif action == "":
            pass_time(20)
            print("you rest for 20 minutes")
            t.sleep(GAME_SPEED)
        elif action == "cheat":
            Statistics.cheats = "Yes"
            P.health = P.max_health
            P.hunger = P.max_hunger
