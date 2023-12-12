def getStartAndEndPoints():
    """
    This function gets the start and end points of the route from the user.
    It then returns the start and end points as a tuple.
    """
    start = input("Enter the starting point of the route: ")
    end = input("Enter the ending point of the route: ")
    return (start, end)


def getRoute(start, end):
    """
    This function takes in the start and end points of the route and returns
    the route as a list of tuples.
    """
    route = []
    url = (
        "https://maps.googleapis.com/maps/api/directions/json?origin="
        + start
        + "&destination="
        + end
        + "&key="
        + API_KEY
    )
    response = requests.get(url)
    data = json.loads(response.text)
    for step in data["routes"][0]["legs"][0]["steps"]:
        route.append(step["html_instructions"])
    return route


def getDirections(route):
    """
    This function takes in the route as a list of tuples and prints out the
    directions.
    """
    directions = []
    print("\nDIRECTIONS:\n")
    for step in route:
        directions.append(step)
    return directions


def writePathToFile(directions, start, end):
    """
    This function takes the directions as a list of tuples, and the start/endpoint as a string
    and writes the directions to a file.
    """
    with open("directions.txt", "w") as f:
        f.write("DIRECTIONS FROM " + start + " TO " + end + "\n\n")
        for step in directions:
            soup = BeautifulSoup(step, "html.parser")
            f.write(soup.text + "\n\n")


def showDirections(directions):
    """
    This function takes in the directions as a list of tuples and prints out
    the directions.
    """
    for step in directions:
        soup = BeautifulSoup(step, "html.parser")
        print(soup.text)


def getDistance(start, end):
    """
    This function takes in the route as a list of tuples and returns the
    distance of the route.
    """
    distance = 0
    url = (
        "https://maps.googleapis.com/maps/api/directions/json?origin="
        + start
        + "&destination="
        + end
        + "&key="
        + API_KEY
    )
    response = requests.get(url)
    data = json.loads(response.text)
    for step in data["routes"][0]["legs"][0]["steps"]:
        distance += step["distance"]["value"]

    distance = distance / 1609.34
    return distance


def getDuration(start, end):
    """
    This function takes in the route as a list of tuples and returns the
    duration of the route.
    """
    duration = 0
    url = (
        "https://maps.googleapis.com/maps/api/directions/json?origin="
        + start
        + "&destination="
        + end
        + "&key="
        + API_KEY
    )
    response = requests.get(url)
    data = json.loads(response.text)
    for step in data["routes"][0]["legs"][0]["steps"]:
        duration += step["duration"]["value"]
    duration = duration / 60 / 60
    duration = round(duration, 2)
    return duration


def getEcoRoute(start, end):
    """This function uses the google maps route API to send a request for an
    eco-friendly route. It returns the route as a list of tuples.
    """
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.routeLabels,routes.routeToken,routes.travelAdvisory.fuelConsumptionMicroliters",
    }
    data = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": 41.76904801292959,
                    "longitude": -72.67374935684933,
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": 41.823042361105024,
                    "longitude": -71.40933143059424,
                }
            }
        },
        "routeModifiers": {"vehicleInfo": {"emissionType": "GASOLINE"}},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
        "extraComputations": ["FUEL_CONSUMPTION"],
        "requestedReferenceRoutes": ["FUEL_EFFICIENT"],
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}\n{response.text}")


def getCarbonEmission(distance):
    """
    This function takes in the distance of the route and returns the carbon
    emission of the route using the EPA API
    """
    url = (
        "https://api.triptocarbon.xyz/v1/footprint?activity="
        + distance
        + "&activityType=miles&country=usa&mode=bus&fuelType=gasoline&"
        + "vehicleEfficiency=20&isPublicTransport=false&planeSeatClass=economy"
    )
    response = requests.get(url)
    data = json.loads(response.text)
    carbonEmission = data["carbonFootprint"]
    return carbonEmission


def decisionTreeToGetCarbonEmission(distance):
    pass
