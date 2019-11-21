# Current data format for cityIO as used in CSL

## grid

Grid is an array (number of elements = "header/spatial/ncols" * "header/spatial/nrows". In our case 72 * 48 right now of 2-element-arrays.) Starting from the top-left, increasing along a row, then iterating the column.

So ```idx=x+y*ncols```, or the other way round: ```x=idx%ncols; y=idx%nrows```

```json
"grid" = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[1,2],[1,3],[2,0],[2,1],[2,0],[1,0],[1,2],[1,2],[0,0],[1,0],[1,1],[1,0],[1,3],[4,0],[2,0],[1,3],[1,1],[1,3],[0,0],[1,3],[1,2],[1,3],[1,1],[1,1],[2,0],[1,3],[3,3],[2,0],[3,3],[3,0],[5,0],[0,0],[2,1],[2,1],[2,0],[2,1],[3,1],[3,2],[3,1],[3,3],[3,0],[3,1],[3,1],[3,0],[2,1],[2,0],[3,3],[3,2],[3,1],[1,1],[1,3],[3,2],[3,3],[3,2] ...
```

## block

The following tells us what the two elements in each grid cell mean (as before). We don't care about rotation right now.
```"header/block" = ["type","rotation"]```

### type mapping

Consequently, the first number in each grid cell defines it's type as an array index of the following list of occuring types (excerpt). This list is automatically updated by the front-end, if an unseen property combination occurs. The order of elements is arbitrary and depends on the user input.

### edge cases

Some cases should not happen, which we have to catch in the front-end and possibly modules, i.e.:

* ```type[idx] = {}``` this showed up sometimes in our mapping. I'm not quite sure yet, how and why :P
* ```type[idx]["type"] == "building" && "str_bike" in type[idx]``` or any other combination of properties of two disjunct types. Modules should be able to be agnostic about the possible combinations and jsut look for all cell with relevant information for their case. E.g. the noise module uses all cells with ```type[idx]["type"] == "building"``` and a module that calculates car traffic only cells with ```type[idx]["str_numLanes"] > 0```.
* ```type[idx]["bld_useGround"] = null``` null values are a bit of an issue when parsing goes wrong. We try to make the user unable to input this, but modules should implement robust array access. ```type[idx]["bld_useUpper"] = null on the other hand is expected, when a building has only one level.
* ```type[idx]["bld_numLevels"] == 0``` This makes no sense, of course. We try to make this impossible via the front-end. So far this only immediately affects the noise module.

### sample mapping

```json
"header/mapping/type" = [{
	"type": "empty"
}, {
	"str_bike": true,
	"str_elevator": false,
	"str_numLanes": 0,
	"str_ramp": false,
	"str_speed": 50,
	"str_stairs": true,
	"type": "street"
}, {
	"bld_numLevels": 14,
	"bld_useGround": "commercial",
	"bld_useUpper": "office",
	"type": "building"
}, {
	"os_type": "green_space",
	"type": "open_space"
}, {
	"str_bike": true,
	"str_elevator": false,
	"str_numLanes": 2,
	"str_ramp": false,
	"str_speed": 50,
	"str_stairs": false,
	"type": "street"
}, {
	"bld_numLevels": 19,
	"bld_useGround": "residential",
	"bld_useUpper": "residential",
	"type": "building"
}, {
	"bld_numLevels": 30,
	"bld_useGround": "commercial",
	"bld_useUpper": "office",
	"type": "building"
}, {
	"os_type": "water",
	"type": "open_space"
}, {
	"str_bike": false,
	"str_elevator": false,
	"str_numLanes": 2,
	"str_ramp": false,
	"str_speed": 50,
	"str_stairs": false,
	"type": "street"
}, {
	"bld_numLevels": 34,
	"bld_useGround": "office",
	"bld_useUpper": "office",
	"type": "building"
}, {
	"os_type": "playground",
	"type": "open_space"
}
```

## sample code

Some sample [code](https://github.com/grasbrook-cityscope/pyGraKPI) on how to work with this in python:

```python
# data is the json from cityIO decoded into a dictionary
gridData = data["grid"]
mapping = data["header"]["mapping"]["type"]
typeidx = data["header"]["block"].index("type")

typejs = {
    "white" : ["building"],
    "grey" : ["street"]
} # this defines all the types we are interested in
    
for cell in gridData:
    if(cell is None or not "type" in mapping[cell[gridDef.typeidx]]): continue

    curtype = gridDef.mapping[cell[gridDef.typeidx]]["type"]
    if curtype in typejs["white"]:
        handleWhiteWater()
    elif curtype in typejs["grey"]:
        handleGreyWater()
    else:
        handleUnknownWater()
```

A slightly more complex [program](https://github.com/grasbrook-cityscope/pyGraKPI) might look like this:

```python
cellSize = data["header"]["spatial"]["cellSize"]

typejs = {
    "buildinguses" : {
        "living" : ["residential"],
        "commerce" : ["office","commercial"],
        "special" : ["educational","culture"]
    },
    "openspacetypes" : {
        "green" : ["green_space"],
        "sports": ["athletic_field"],
        "playgrounds":["daycare_playground","playground","schoolyard"],
        "other":["exhibition_space","recycling_center","promenade","water"]
    }
}

for cell in gridData:
    if(cell is None or not "type" in mapping[cell[typeidx]]): continue
    cur_type = mapping[cell[typeidx]]["type"]

    if cur_type == "building":
        cur_use_ground = mapping[cell[typeidx]]["bld_useGround"]
        cur_use_top = mapping[cell[typeidx]]["bld_useUpper"]
        cur_bld_levels = mapping[cell[typeidx]]["bld_numLevels"]

        if cur_use_ground and cur_bld_levels > 0:
            if cur_use_ground in typejs["buildinguses"]["living"]:
                bld_living += cellSize*cellSize
            if cur_use_ground in typejs["buildinguses"]["commerce"]:
                bld_commerce += cellSize*cellSize
            if cur_use_ground in typejs["buildinguses"]["special"]:
                bld_special += cellSize*cellSize

        if cur_use_top and cur_bld_levels > 1:
            if cur_use_top in typejs["buildinguses"]["living"]:
                bld_living += cellSize*cellSize * (cur_bld_levels - 1)
            if cur_use_top in typejs["buildinguses"]["commerce"]:
                bld_commerce += cellSize*cellSize * (cur_bld_levels - 1)
            if cur_use_top in typejs["buildinguses"]["special"]:
                bld_special += cellSize*cellSize * (cur_bld_levels - 1)
```