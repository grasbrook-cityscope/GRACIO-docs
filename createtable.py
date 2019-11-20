import requests
import json
import urllib

def getCurrentState(fromwhere):
    with urllib.request.urlopen(fromwhere) as url:
        return json.loads(url.read().decode())
    return None

def read_json_file(settings_file):
        # open json file
        with open(settings_file) as d:
            data = json.load(d)
        return(data)

def send_json_to_cityIO(cityIO_json, name):
        # defining the api-endpoint
        post_address = "https://cityio.media.mit.edu/api/table/update/" + name

        r = requests.post(post_address, json=cityIO_json, headers={'Content-Type': 'application/json'})
        print(r)
        if not r.status_code == 200:
            print("could not post result to cityIO")
            print("Error code", r.status_code)
        else:
            print("Successfully posted to cityIO", r.status_code)


def change_grid(name, cell = 0, value = [1,0]):

    grid = getCurrentState("https://cityio.media.mit.edu/api/table/"+name+"/grid")

    # defining the api-endpoint
    post_address = "https://cityio.media.mit.edu/api/table/update/" + name + "/grid"

    if grid[cell] == value:
        grid[cell] = [0,0]
    else:
        grid[cell] = value

    r = requests.post(post_address, json=grid, headers={'Content-Type': 'application/json'})
    print(r)
    if not r.status_code == 200:
        print("could not post result to cityIO")
        print("Error code", r.status_code)
    else:
        print("Successfully posted to cityIO", r.status_code)

def fill_grid(name,value = [0,0]):
    grid = getCurrentState("https://cityio.media.mit.edu/api/table/"+name+"/grid")
    types = getCurrentState("https://cityio.media.mit.edu/api/table/"+name+"/header/mapping/type")

    # defining the api-endpoint
    post_address = "https://cityio.media.mit.edu/api/table/update/" + name + "/grid"

    it = 0
    for cell in grid:
        if cell is None:
            grid[it] = value
            print("fill")
        elif cell[0] >= len(types):
            print(cell)
            grid[it] = value
        it+=1

    r = requests.post(post_address, json=grid, headers={'Content-Type': 'application/json'})
    print(r)
    if not r.status_code == 200:
        print("could not post result to cityIO")
        print("Error code", r.status_code)
    else:
        print("Successfully posted to cityIO", r.status_code)


def change_header(name, field, value):
    header = getCurrentState("https://cityio.media.mit.edu/api/table/"+name+"/header")
    post_address = "https://cityio.media.mit.edu/api/table/update/" + name + "/header"

    fields = field.split("/")
    
    if len(fields) == 1:
        header[fields[0]] = value
    elif len(fields) == 2:
        header[fields[0]][fields[1]] = value
    elif len(fields) == 3:
        header[fields[0]][fields[1]][fields[2]] = value

    # print(header)
    r = requests.post(post_address, json=header, headers={'Content-Type': 'application/json'})
    print(r)
    if not r.status_code == 200:
        print("could not post result to cityIO")
        print("Error code", r.status_code)
    else:
        print("Successfully posted to cityIO", r.status_code)


if __name__ == "__main__":
    # data = read_json_file("sampletable.json")

    # print(data["header"])

    # send_json_to_cityIO(data,"grasbrook_test")
    mapping = [
        {"type":"empty"},
        {"str_bike":True,"str_elevator":False,"str_numLanes":0,"str_ramp":False,"str_speed":50,"str_stairs":True,"type":"street"},
        {"bld_numLevels":14,"bld_useGround":"commercial","bld_useUpper":"office","type":"building"},
        {"os_type":"green_space","type":"open_space"},
        {"str_bike":True,"str_elevator":False,"str_numLanes":2,"str_ramp":False,"str_speed":50,"str_stairs":False,"type":"street"},
        {"bld_numLevels":19,"bld_useGround":"residential","bld_useUpper":"residential","type":"building"},
        {"bld_numLevels":11,"bld_useGround":"residential","bld_useUpper":"residential","type":"building"},
        {"bld_numLevels":0,"bld_useGround":"residential","bld_useUpper":"residential","type":"building"},
        {"bld_numLevels":9,"bld_useGround":"residential","bld_useUpper":"residential","type":"building"},
        {"bld_numLevels":0,"bld_useGround":"office","bld_useUpper":"office","type":"building"},
        # {"bld_numLevels":0,"bld_useGround":null,"bld_useUpper":null,"type":"building"},
        {"bld_numLevels":51,"bld_useGround":"commercial","bld_useUpper":"commercial","type":"building"},
        {"bld_numLevels":30,"bld_useGround":"commercial","bld_useUpper":"office","type":"building"},
        # {"bld_numLevels":12,"bld_useGround":null,"bld_useUpper":"office","type":"building"},
        # {"bld_numLevels":1,"bld_useGround":null,"bld_useUpper":"office","type":"building"},
        # {"bld_numLevels":1,"bld_useGround":"residential","bld_useUpper":null,"type":"building"},
        {"os_type":"water","type":"open_space"},
        # {},
        {"str_bike":False,"str_elevator":False,"str_numLanes":2,"str_ramp":False,"str_speed":50,"str_stairs":False,"type":"street"},
        {"bld_numLevels":34,"bld_useGround":"office","bld_useUpper":"office","type":"building"}]
    
    # change_header("grasbrook_test","mapping/type",mapping)
    # change_header("grasbrook_test","spatial/ncols",78)
    # change_header("grasbrook_test","spatial/nrows",43)

    # grid in front-end: 78*44
    # fill_grid("grasbrook_test")

    # upper left corner of grid in front-end: 53.53764806145533 10.00736954095224
    # change_header("grasbrook_test","spatial/latitude",53.53764806145533)
    # change_header("grasbrook_test","spatial/longitude",10.00736954095224)
    # bottom left corner of grid in front-end 53.526354, 10.016304
    # change_header("grasbrook_test","spatial/latitude",53.526354)
    # change_header("grasbrook_test","spatial/longitude",10.016304)
    
    # change_grid("grasbrook_test")


