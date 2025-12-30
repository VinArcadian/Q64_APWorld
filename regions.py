from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import Quest64World

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: Quest64World) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: Quest64World) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    earth_region = Region("Earth Region", world.player, world.multiworld)
    wind_region = Region("Wind Region", world.player, world.multiworld)
    water_region = Region("Water Region", world.player, world.multiworld)
    fire_region = Region("Fire Region", world.player, world.multiworld)
    book_region = Region("Book Region", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [earth_region, wind_region, water_region, fire_region, book_region]

    ## Some regions may only exist if the player enables certain options.
    ## In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # if world.options.hammer:
    #    top_middle_room = Region("Top Middle Room", world.player, world.multiworld)
    #    regions.append(top_middle_room)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: Quest64World) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    earth_region = world.get_region("Earth Region")
    wind_region = world.get_region("Wind Region")
    water_region = world.get_region("Water Region")
    fire_region = world.get_region("Fire Region")
    book_region = world.get_region("Book Region")

    ## Okay, now we can get connecting. For this, we need to create Entrances.
    ## Entrances are inherently one-way, but crucially, AP assumes you can always return to the origin region.
    ## One way to create an Entrance is by calling the Entrance constructor.
    # earth_region_to_wind_region = Entrance(world.player, "Earth Region to Wind Region", parent=earth_region)
    # earth_region.exits.append(earth_region_to_wind_region)

    ## You can then connect the Entrance to the target region.
    # earth_region_to_wind_region.connect(wind_region)

    # An even easier way is to use the region.connect helper.
    wind_region.connect(water_region, "Wind Region to Water Region")
    water_region.connect(fire_region, "Water Region to Fire Region")

    # The region.connect helper even allows adding a rule immediately.
    # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    earth_region.connect(wind_region, "Earth Region to Wind Region", lambda state: state.has("Earth Orb", world.player))
    wind_region.connect(water_region, "Wind Region to Water Region", lambda state: state.has("Wind Jade", world.player))
    water_region.connect(fire_region, "Water Region to Fire Region", lambda state: state.has("Water Jewel", world.player))
    fire_region.connect(book_region, "Fire Region to Book Region", lambda state: state.has("Fire Ruby", world.player))
    

    ## Some Entrances may only exist if the player enables certain options.
    ## In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    ## In this case, we previously created an extra "Top Middle Room" region that we now need to connect to Overworld.
    # if world.options.hammer:
    #    top_middle_room = world.get_region("Top Middle Room")
    #    overworld.connect(top_middle_room, "Overworld to Top Middle Room")