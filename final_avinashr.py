import json
import requests
from bs4 import BeautifulSoup
from Secrets import API_KEY, HERE_API_KEY
from pprint import pprint
from datetime import datetime


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


def getDistance(start, end, initVal=0, flag=False):
    """
    This function takes in the route as a list of tuples and returns the
    distance of the route.
    """
    if flag:
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
    else:
        distance = initVal

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


def getCoordinates(start, end):
    """
    This function takes in the route as a list of tuples and returns the
    coordinates of the route.
    """
    coordinates = []
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
        coordinates.append(step["start_location"])
    return [coordinates[0], coordinates[-1]]


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
                    "latitude": start["lat"],
                    "longitude": start["lng"],
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": end["lat"],
                    "longitude": end["lng"],
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


def getCarbonEmission(distance, preferences):
    """
    This function takes in the distance of the route and returns the carbon
    emission of the route using the EPA API
    """

    url = (
        "https://api.triptocarbon.xyz/v1/footprint?activity="
        + distance
        + f"&activityType=miles&country=usa&mode={preferences['vehicleType']}&fuelType={preferences['fuelType']}&"
        + "vehicleEfficiency=20&isPublicTransport=false"
    )
    response = requests.get(url)
    data = json.loads(response.text)
    carbonEmission = data["carbonFootprint"]
    return carbonEmission


def getEcoCarbonEmission(distance):
    """
    This function takes in the distance of the route and returns the carbon
    emission of the route using the EPA API
    """

    url = (
        "https://api.triptocarbon.xyz/v1/footprint?activity="
        + distance
        + "&activityType=miles&country=usa&mode=bus&fuelType=diesel&"
        + "vehicleEfficiency=20&isPublicTransport=true"
    )
    response = requests.get(url)
    data = json.loads(response.text)
    carbonEmission = data["carbonFootprint"]
    return carbonEmission


def createGraph():
    """
    This function asks the user about their transportation preferences and
    creates a graph of the preferences, such as vehicle type, fule type and so on.
    Returns the graph.
    """

    print(
        "Please answer the following questions to help us determine your transportation preferences."
    )
    vehicleType = input(
        "What type of vehicle do you drive? dieselCar, petrolCar, taxi, motorbike, bus: "
    )
    fuelType = input(
        "What type of fuel does your vehicle use? motorGasoline (petrol), diesel:  "
    )
    fuelEfficiency = input(
        "What is the fuel efficiency of your vehicle? (in miles per gallon) "
    )
    publicTransport = input("Do you use public transport? (yes/no) ")
    if publicTransport == "yes":
        publicTransportType = input(
            "What type of public transport do you use? (bus, train, etc.) "
        )
        publicTransportEfficiency = input(
            "What is the fuel efficiency of your public transport? (in miles per gallon) "
        )
    else:
        publicTransportType = None
        publicTransportEfficiency = None
    graph = {
        "vehicleType": vehicleType,
        "fuelType": fuelType,
        "fuelEfficiency": fuelEfficiency,
        "publicTransport": publicTransport,
        "publicTransportType": publicTransportType,
        "publicTransportEfficiency": publicTransportEfficiency,
    }
    return graph


def getPublicTransportInfo(start, end):
    url = (
        "https://transit.router.hereapi.com/v8/routes?apiKey="
        + HERE_API_KEY
        + "&origin="
        + f"{start['lat']},{start['lng']}"
        + "&destination="
        + f"{end['lat']},{end['lng']}"
    )
    response = requests.get(url)
    data = json.loads(response.text)
    return data


def format_time(time_string):
    dt_object = datetime.fromisoformat(time_string.replace("Z", "+00:00"))
    return dt_object.strftime("%Y-%m-%d %H:%M:%S %Z")


def displayPublicTransportInfo(data):
    for route in data["routes"]:
        print(f"Route ID: {route['id']}")
        print("Transport Options:")
        for section in route["sections"]:
            transport = section.get("transport", {})
            if transport:
                print(f"  - Mode: {transport['mode']}")
                if transport["mode"] == "transit":
                    print(f"    Name: {transport.get('name', 'N/A')}")
                    print(f"    Category: {transport.get('category', 'N/A')}")
                    print(f"    Headsign: {transport.get('headsign', 'N/A')}")
                    agency = section.get("agency", {})
                    print(
                        f"    Agency: {agency.get('name', 'N/A') if agency else 'N/A'}"
                    )
                    print(f"    Agency Website: {agency.get('website', 'N/A')}")
                departure = section.get("departure", {})
                arrival = section.get("arrival", {})
                if departure:
                    print(f"    Departure Time: {format_time(departure['time'])}")
                    departure_place = departure.get("place", {})
                    if departure_place:
                        print(
                            f"    Departure Place: {departure_place.get('name', 'N/A')}"
                        )
                if arrival:
                    print(f"    Arrival Time: {format_time(arrival['time'])}")
                    arrival_place = arrival.get("place", {})
                    if arrival_place:
                        print(f"    Arrival Place: {arrival_place.get('name', 'N/A')}")


def __main__():
    start, end = getStartAndEndPoints()
    route = getRoute(start, end)
    showDirections(getDirections(route))
    distance = getDistance(start, end, flag=True)
    duration = getDuration(start, end)
    print("\nThe total distance of the route is: " + str(distance) + " miles")
    print("\nThe total duration of the route is: " + str(duration) + " hour(s)")

    print("\nUser preferences:\n")
    graphPreferences = createGraph()

    carbonEmission = getCarbonEmission(str(distance), graphPreferences)
    print(
        "The total carbon emission of the route is: " + str(carbonEmission) + " pounds"
    )

    startCoord, endCoord = getCoordinates(start, end)

    print("\nEco-friendly route:\n")
    ecoRoute = getEcoRoute(startCoord, endCoord)
    # print(ecoRoute)

    print(
        "Distance of Eco-Route: "
        + str(
            getDistance(
                None, None, initVal=ecoRoute["routes"][0]["distanceMeters"], flag=False
            )
        )
        + " miles"
    )
    # showDirections(getDirections(ecoRoute))
    print(
        "Carbon emission of eco-route via bus would be",
        getEcoCarbonEmission(str(int(distance))),
        "pounds",
    )

    print("\nPublic transport info:\n")
    publicTransportInfo = getPublicTransportInfo(startCoord, endCoord)
    # pprint(publicTransportInfo)
    displayPublicTransportInfo(publicTransportInfo)

    saveToFile = input("\nWould you like to save the directions to a file? (y/n) ")
    if saveToFile == "y":
        writePathToFile(getDirections(route), start, end)
        print("\nDirections saved to file\n")
    else:
        print("\nDirections not saved to file\n")


if __name__ == "__main__":
    __main__()
