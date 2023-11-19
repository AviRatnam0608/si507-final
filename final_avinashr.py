import json
import requests
from Secrets import API_KEY


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
    print("\nDIRECTIONS:\n")
    for step in route:
        print(step)
    print("\n")


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
    return duration


def __main__():
    start, end = getStartAndEndPoints()
    route = getRoute(start, end)
    getDirections(route)
    distance = getDistance(start, end)
    duration = getDuration(start, end)
    print("The total distance of the route is: " + str(distance) + " meters")
    print("The total duration of the route is: " + str(duration) + " seconds")


if __name__ == "__main__":
    __main__()
