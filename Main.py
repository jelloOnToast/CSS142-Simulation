import simpy
import random
import uuid
import matplotlib.pyplot as plt
import networkx as nx

# Redefine the classes with slight modifications for SimPy and data collection

class Ticket:
    def __init__(self, ticketId, passengerId, busId, validity):
        self.ticketId = ticketId
        self.passengerId = passengerId
        self.busId = busId
        self.validity = validity
    
    def verifyTicket(self):
        return self.validity

class PaymentApp:
    def __init__(self, appId, appName):
        self.appId = appId
        self.appName = appName
        self.verifiedPayments = []
    
    def processPayment(self, passengerId, busId):
        # Simulate payment processing
        paymentId = uuid.uuid4()
        self.verifiedPayments.append((paymentId, passengerId, busId))
        return True
    
    def generateTicket(self, passengerId, busId):
        # Simulate ticket generation
        ticketId = uuid.uuid4()
        return Ticket(ticketId, passengerId, busId, True)

class Passenger:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.busId = None
    
    def purchaseTicket(self, payment_app, busId):
        if payment_app.processPayment(self.id, busId):
            return payment_app.generateTicket(self.id, busId)
        return None
    
    def boardBus(self, ticket, bus):
        if bus.boardPassenger(ticket):
            self.busId = bus.busId
            print(f"Passenger {self.name} boarded the bus {bus.busId}.")
        else:
            print(f"Passenger {self.name} could not board the bus {bus.busId} due to full capacity or invalid ticket.")
    
    def alightBus(self, bus):
        if self.busId == bus.busId:
            bus.alightPassenger(self.id)
            self.busId = None
            print(f"Passenger {self.name} alighted the bus {bus.busId}.")

class Bus:
    def __init__(self, env, busId, capacity, transit_data):
        self.env = env
        self.busId = busId
        self.capacity = capacity
        self.passengers = []
        self.location = "Main Terminal"
        self.route = ["Main Terminal", "Stop 1", "Stop 2", "Stop 3"]
        self.route_index = 0
        self.control_system = None
        self.transit_data = transit_data
    
    def updateLocation(self):
        self.route_index = (self.route_index + 1) % len(self.route)
        self.location = self.route[self.route_index]
        print(f"Bus {self.busId} moved to {self.location} at time {self.env.now}")
        if self.control_system:
            self.control_system.receiveBusLocation(self.busId, self.location)
        self.transit_data['bus_locations'].append((self.env.now, self.busId, self.location))
    
    def communicateWithControlSystem(self, control_system):
        self.control_system = control_system
        control_system.receiveBusLocation(self.busId, self.location)
    
    def boardPassenger(self, ticket):
        if len(self.passengers) < self.capacity and ticket.busId == self.busId:
            self.passengers.append(ticket.passengerId)
            self.transit_data['passenger_bus'].append((self.env.now, ticket.passengerId, self.busId))
            return True
        return False
    
    def alightPassenger(self, passengerId):
        if passengerId in self.passengers:
            self.passengers.remove(passengerId)
            self.transit_data['passenger_bus'].append((self.env.now, passengerId, None))
    
    def run(self):
        while True:
            self.updateLocation()
            yield self.env.timeout(5)  # Move to the next stop every 5 time units

class CentralizedControlSystem:
    def __init__(self, env, systemId, transit_data):
        self.env = env
        self.systemId = systemId
        self.busLocations = {}
        self.transit_data = transit_data
    
    def manageSchedule(self):
        print("Managing bus schedule.")
    
    def provideRouteInfo(self):
        print("Providing route information.")
    
    def monitorTraffic(self):
        print("Monitoring traffic conditions.")
    
    def receiveBusLocation(self, busId, location):
        self.busLocations[busId] = location
        print(f"Bus {busId} is currently at {location} at time {self.env.now}")
        self.transit_data['bus_locations'].append((self.env.now, busId, location))
    
    def run(self):
        while True:
            self.monitorTraffic()
            yield self.env.timeout(10)  # Monitor traffic every 10 time units

# Initialize simulation environment
env = simpy.Environment()

# Initialize data collection
transit_data = {
    'bus_locations': [],
    'passenger_bus': []
}

# Create buses
bus1 = Bus(env, 101, 2, transit_data)
bus2 = Bus(env, 102, 2, transit_data)

# Create centralized control system
control_system = CentralizedControlSystem(env, 1, transit_data)

# Buses communicate with control system
bus1.communicateWithControlSystem(control_system)
bus2.communicateWithControlSystem(control_system)

# Create passengers
passenger1 = Passenger(1, "John Doe", "john@example.com")
passenger2 = Passenger(2, "Jane Smith", "jane@example.com")
passenger3 = Passenger(3, "Alice Johnson", "alice@example.com")
passenger4 = Passenger(4, "Bob Brown", "bob@example.com")

# Create payment app
payment_app = PaymentApp(1, "EZPay")

# Simulate passenger actions
def passenger_actions(env, passenger, payment_app, bus):
    ticket = passenger.purchaseTicket(payment_app, bus.busId)
    yield env.timeout(random.randint(1, 5))  # Wait before boarding
    passenger.boardBus(ticket, bus)
    yield env.timeout(random.randint(5, 10))  # Stay on bus for a while
    passenger.alightBus(bus)

# Add processes to the environment
env.process(bus1.run())
env.process(bus2.run())
env.process(control_system.run())
env.process(passenger_actions(env, passenger1, payment_app, bus1))
env.process(passenger_actions(env, passenger2, payment_app, bus1))
env.process(passenger_actions(env, passenger3, payment_app, bus2))
env.process(passenger_actions(env, passenger4, payment_app, bus2))

# Run the simulation
env.run(until=30)

# Visualize the transit system
def plot_transit_system(transit_data):
    G = nx.DiGraph()

    # Add bus stops
    stops = ["Main Terminal", "Stop 1", "Stop 2", "Stop 3"]
    for stop in stops:
        G.add_node(stop, pos=(stops.index(stop) * 2, 0))

    # Add buses and their movements
    for time, busId, location in transit_data['bus_locations']:
        if location in stops:
            G.add_node(f"{busId}-{time}", pos=(stops.index(location) * 2, time))
            G.add_edge(location, f"{busId}-{time}", color='blue')
            if time > 0:
                prev_time = time - 5
                G.add_edge(f"{busId}-{prev_time}", f"{busId}-{time}", color='blue')

    # Add passengers and their movements
    for time, passengerId, busId in transit_data['passenger_bus']:
        if busId:
            location = next(loc for t, b, loc in transit_data['bus_locations'] if b == busId and t == time)
            G.add_node(f"{passengerId}-{time}", pos=(stops.index(location) * 2, time))
            G.add_edge(location, f"{passengerId}-{time}", color='red')
        else:
            G.add_node(f"{passengerId}-{time}", pos=(stops.index(location) * 2, time))

    pos = nx.get_node_attributes(G, 'pos')
    colors = [G[u][v]['color'] for u, v in G.edges()]

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', edge_color=colors, node_size=500, font_size=10)
    plt.title("EDSA Carousel Bus Transit System Simulation")
    plt.show()

plot_transit_system(transit_data)
