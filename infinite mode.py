from commands import *

clear_console()
P.name = "David"
world_generation = [town, forest, forest]

P.weapons[0] = c.deepcopy(table_leg)
P.weapons[1] = fists
P.weapons[2] = fists
location = town


while True:
    def options():
        print("1 -inventory")
        print("2 -search for buildings")
        print("3 -travel")


    print("you arrived at", location.name)
    t.sleep(game_speed)
    stay = True
    travel_options = [r.choice(world_generation) for i in range(3)]
    travel_distances = [r.randint(3, 6), r.randint(4, 8), r.randint(5, 10)]
    buildings = r.choices(location.structures, location.structure_weights, k=location.size)
    while stay:
        player_info()
        options()
        action = myinput([1, 2, 3, ""])
        if action == 1:  # inventory
            open_inventory()
        elif action == 2:  # search for building
            if round(P.inventory_used) <= P.inventory_capacity:
                if len(buildings) <= 0:
                    print("you explored everything")
                    t.sleep(game_speed)
                else:
                    pass_time(10)
                    if (len(buildings) / location.size) > r.random():
                        building = r.choice(buildings)
                        buildings.remove(building)
                        print("you found", building.name)
                        t.sleep(game_speed)
                        enemy_count = r.randint(round(building.danger / 2), round(building.danger))
                        print("you can see {} enemies".format(enemy_count))
                        t.sleep(game_speed)
                        print("0 -go away")
                        print("1 -go inside")
                        choice = myinput([0, 1])
                        if choice == 1:
                            fight(enemy_count=enemy_count)
                            loot = r.choices(building.loot, building.loot_weight,
                                             k=r.randint(building.size, round(building.size * 1.5)))
                            clear_console()
                            print("you search the building")
                            t.sleep(game_speed)
                            for item in loot:
                                get_item(item)
                    else:
                        print("you didn't find anything")
                        t.sleep(game_speed)
            else:
                print("you carry too much items")
                t.sleep(game_speed)
        elif action == 3:  # travel
            if P.inventory_used <= P.inventory_capacity:
                print("you can travel to:")
                for i in range(len(travel_options)):
                    print("  {}) {} - {}km".format(i + 1, travel_options[i].name, travel_distances[i]))
                selected = myinput([0, 1, 2, 3])
                if selected == 0:
                    player_info()
                    options()
                else:
                    travel = 1
                    hunger_cost = travel_distances[selected - 1] * 20 * P.hunger_modifier
                    if hunger_cost > P.hunger:
                        print("you don't have enough hunger")
                        print("0 -stay")
                        print("1 -continue")
                        travel = myinput([0, 1])
                    if travel == 1:
                        print("you travel to", travel_options[selected - 1].name)
                        stay = False
                        pass_time(travel_distances[selected - 1] * 20)
                        location = travel_options[selected - 1]
            else:
                print("you carry too much items")
                t.sleep(game_speed)
        elif action == "":
            pass_time(10)
            print("you rest")
            t.sleep(game_speed)
