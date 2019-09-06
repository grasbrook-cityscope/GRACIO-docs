# GRACIO
Repo for documentation and specification of GRACIO/Grasbrook CityScopes


## Description

...

## Infrastracture

![architecture schematic](figures/infrastructure_schematic_wb.jpg "architecture schematic")

[CityIO](https://github.com/CityScope/CS_CityIO) is the central point of knowledge. All data is stored there. [table data](https://cityio.media.mit.edu/api/table/grasbrook/)
the front-end and some simulation models require the grid to be represented as geodata (GeoJSON). [CityIO_to_geoJSON](https://github.com/andredaa/city_io_to_geojson) does the conversion from table meta parameters (lat, lon, number of cells/rows, cell dimensions) to a GeoJSON containing the right set of quadruatic polygons.

## Interfaces

- grid as array of ```{type:int, rotation:int}```, index reference frame
- grid as GeoJSON, geo reference frame
- simulation outpus as various (preferably GeoJSON?)

## Cell Properties
Cells are represented in CityIO by their array index, a rotation (int) and a type (int).
Types can be a big number of (almost) arbitrary property combinations (i.e. ```isBuilding=true``` and ```numStories=4```). These properties might have conditions to be applicable (i.e. numStores is only relevant for buildings).
The mapping from the integer type stored in the grid to the actual dictionary of properties set should be represented by hashing. That means every unique combination of properties has a unique hash.

That means we need:
- a database storing property dictionaries to the hashes
- a service translating hashes to dictionaries and vice-versa, so other software components (front-end, simulation modules) don't have to know the database structure

Also, the names and the possible values and the conditions of properties have to be specifically defined and immutable! Otherwise the front-end doesn't know what UI-elements to display and the simulation models don't know what values they can work with.

[Draft for possible properties](https://docs.google.com/spreadsheets/d/1DOxu__JDZzfLnyQFTfZ7T8ndZIsdYotxPbvtF2Q_o_I/edit#gid=0)

## To Do

### specification
- define user-changeble parameters (see "Cell Properties" above)
- figure out architecture for hashing properties
- decide on wether GeoJSON grids contain properties or if they should be obtained from the grid array instead (reasoning: geoJSONs get really big, might make sense to only create on at startup and get/send data only on index-referenced-grid basis)

### front-end
- select grid cells
- change params for grid cells
- previous states of grid?

### CityIO
- one dataset for each user
- authenticating users
- keep previous states of grid?

### Simulation modules
- define required parameters
- define inferred and assumed parameters
- make noise simulation interface nicely
- write more