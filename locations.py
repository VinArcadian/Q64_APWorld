from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import Quest64World

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {
    "Melrode Monastery - Garden Chest": 1,
    "Melrode Monastery - Cellar Chest 1": 2,
    "Melrode Monastery - Cellar Chest 2": 3,
    "Melrode Monastery - Refectory Chest": 4,
    "Melrode Monastery - Refectory Gift (Pat)": 5,
    "Melrode - Wingsmith (Ingram)": 6,
    "Melrode - Shepard's Hut Chest": 7,
    "Dondoran - Tavern Gift (Mable)": 8,
    "Dondoran - Tavern Gift (Maggie)": 9,
    "Dondoran - Wingsmith (Thom)": 10,
    "Dondoran Castle - Scottford's Bedroom Chest 1": 999,
    "Dondoran Castle - Scottford's Bedroom Chest 2": 999,
    "Dondoran Castle - Scottford's Bedroom Chest 3": 999,
    "Dondoran Castle - Flora's Bedroom Chest 1": 999,
    "Dondoran Castle - Flora's Bedroom Chest 2": 999,
    "Dondoran Castle - Flora's Bedroom Chest 3": 999,
    "Connor Forest - Hut Interior Chest": 999,
    "Connor Forest - Loch Gate Chest": 999,
    "Connor Forest - Fort Left Platform Chest": 999,
    "Connor Forest - Fort Right Platform Chest": 999,
    "Connor Forest - Boss Reward (Solvaring)": 999,
    "Dondoran Castle - Treasure Room Chest 1": 999,
    "Dondoran Castle - Treasure Room Chest 2": 999,
    "Dondoran Castle - Treasure Room Chest 3": 999,
    "Glencoe - Cottage Chest": 999,
    "Cull Hazard - Plateau Rock Chest": 999,
    "Cull Hazard - SE Corner Cave Chest": 999,
    "Cull Hazard - Eastern Lake Shore Chest 1": 999,
    "Cull Hazard - Eastern Lake Shore Chest 2": 999,
    "Cull Hazard - Hill Past Roots Chest": 999,
    "Normoon - Southern Windmill Chest 1": 999,
    "Normoon - Southern Windmill Chest 2": 999,
    "Normoon - Northern Windmill Chest 1": 999,
    "Normoon - Northern Windmill Chest 2": 999,
    "Windward Forest - Cottage Exterior Chest": 999,
    "Windward Forest - Cottage Interior Chest": 999,
    "Larapool - Crystal Well Chest": 999,
    # Location IDs don't need to be sequential, as long as they're unique and greater than 0.
}


# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class Quest64Location(Location):
    game = "Quest 64"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: Quest64World) -> None:
    create_regular_locations(world)
    # create_events(world)


def create_regular_locations(world: Quest64World) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    earth_region = world.get_region("Earth Region")
    wind_region = world.get_region("Wind Region")
    water_region = world.get_region("Water Region")
    fire_region = world.get_region("Fire Region")
    book_region = world.get_region("Book Region")

    ## One way to create locations is by just creating them directly via their constructor.
    # monastery_garden = Quest64Location(
    #    world.player, "Melrode - Monastery Garden Chest", world.location_name_to_id["Melrode - Monastery Garden Chest"], earth_region
    #)

    ## You can then add them to the region.
    #earth_region.locations.append(monastery_garden)

    # A simpler way to do this is by using the region.add_locations helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also need to pass your overridden Location class.
    earth_region_locations = get_location_names_with_ids(
        ["Melrode - Monastery Garden Chest", "Melrode - Monastery Cellar Chest 1", "Melrode - Monastery Cellar Chest 2", "Melrode Monastery - Refectory Chest", "Melrode Monastery - Refectory Gift (Pat)", "Melrode - Shepard's Hut Chest", "Dondoran - Tavern Gift (Mable)", "Dondoran - Tavern Gift (Maggie)", "Dondoran Castle - Scottford's Bedroom Chest 1", "Dondoran Castle - Scottford's Bedroom Chest 2", "Dondoran Castle - Scottford's Bedroom Chest 3", "Dondoran Castle - Flora's Bedroom Chest 1", "Dondoran Castle - Flora's Bedroom Chest 2", "Dondoran Castle - Flora's Bedroom Chest 3", "Connor Forest - Hut Interior Chest", "Connor Forest - Loch Gate Chest", "Connor Forest - Fort Left Platform Chest", "Connor Forest - Fort Right Platform Chest", "Connor Forest - Boss Reward (Solvaring)"]
    )
    earth_region.add_locations(earth_region_locations, Quest64Location)

    wind_region_locations = get_location_names_with_ids(["EXAMPLE_WIND_LOCATION"])
    wind_region.add_locations(wind_region_locations, Quest64Location)

    water_region_locations = get_location_names_with_ids(["EXAMPLE_WATER_LOCATION"])
    water_region.add_locations(water_region_locations, Quest64Location)

    fire_region_locations = get_location_names_with_ids(["EXAMPLE_FIRE_LOCATION"])
    fire_region.add_locations(fire_region_locations, Quest64Location)

    book_region_locations = get_location_names_with_ids(["EXAMPLE_BOOK_LOCATION"])
    book_region.add_locations(book_region_locations, Quest64Location)

    ## Locations may be in different regions depending on the player's options.
    ## In our case, the hammer option puts the Top Middle Chest into its own room called Top Middle Room.
    # top_middle_room_locations = get_location_names_with_ids(["Top Middle Chest"])
    # if world.options.hammer:
    #    top_middle_room = world.get_region("Top Middle Room")
    #    top_middle_room.add_locations(top_middle_room_locations, APQuestLocation)
    # else:
    #    overworld.add_locations(top_middle_room_locations, APQuestLocation)

    ## Locations may exist only if the player enables certain options.
    ## In our case, the extra_starting_chest option adds the Bottom Left Extra Chest location.
    # if world.options.extra_starting_chest:
        ## Once again, it is important to stress that even though the Bottom Left Extra Chest location doesn't always
        ## exist, it must still always be present in the world's location_name_to_id.
        ## Whether the location actually exists in the seed is purely determined by whether we create and add it here.
    #    bottom_left_extra_chest = get_location_names_with_ids(["Bottom Left Extra Chest"])
    #    overworld.add_locations(bottom_left_extra_chest, APQuestLocation)


# def create_events(world: Quest64World) -> None:
    ## Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
    ## In our case, the player must press a button in the top left room to open the final boss door.
    ## AP has something for this purpose: "Event locations" and "Event items".
    ## An event location is no different than a regular location, except it has the address "None".
    ## It is treated during generation like any other location, but then it is discarded.
    ## This location cannot be "sent" and its item cannot be "received", but the item can be used in logic rules.
    ## Since we are creating more locations and adding them to regions, we need to grab those regions again first.
    # top_left_room = world.get_region("Top Left Room")
    # final_boss_room = world.get_region("Final Boss Room")

    ## One way to create an event is simply to use one of the normal methods of creating a location.
    # button_in_top_left_room = Quest64Location(world.player, "Top Left Room Button", None, top_left_room)
    # top_left_room.locations.append(button_in_top_left_room)

    ## We then need to put an event item onto the location.
    ## An event item is an item whose code is "None" (same as the event location's address),
    ## and whose classification is "progression". Item creation will be discussed more in items.py.
    ## Note: Usually, items are created in world.create_items(), which for us happens in items.py.
    ## However, when the location of an item is known ahead of time (as is the case with an event location/item pair),
    ## it is common practice to create the item when creating the location.
    ## Since locations also have to be finalized after world.create_regions(), which runs before world.create_items(),
    ## we'll create both the event location and the event item in our locations.py code.
    # button_item = items.APQuestItem("Top Left Room Button Pressed", ItemClassification.progression, None, world.player)
    # button_in_top_left_room.place_locked_item(button_item)

    ## A way simpler way to do create an event location/item pair is by using the region.create_event helper.
    ## Luckily, we have another event we want to create: The Victory event.
    ## We will use this event to track whether the player can win the game.
    ## The Victory event is a completely optional abstraction - This will be discussed more in set_rules().
    # final_boss_room.add_event(
    #    "Final Boss Defeated", "Victory", location_type=Quest64Location, item_type=items.APQuestItem
    # )

    ## If you create all your regions and locations line-by-line like this,
    ## the length of your create_regions might get out of hand.
    ## Many worlds use more data-driven approaches using dataclasses or NamedTuples.
    ## However, it is worth understanding how the actual creation of regions and locations works,
    ## That way, we're not just mindlessly copy-pasting! :)