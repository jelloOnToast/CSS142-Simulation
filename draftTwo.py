import uuid

class Passenger:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
    
    def purchaseTicket(self, payment_app, busId):
        if payment_app.processPayment(self.id, busId):
            return payment_app.generateTicket(self.id, busId)
        return None
    
    def boardBus(self, ticket, bus_terminal):
        if bus_terminal.verifyTicket(ticket):
            print(f"Passenger {self.name} boarded the bus.")
        else:
            print(f"Passenger {self.name} could not board the bus due to invalid ticket.")
    
    def alightBus(self, bus):
        bus.alightPassenger(self.id)
        print(f"Passenger {self.name} alighted the bus.")

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

class Ticket:
    def __init__(self, ticketId, passengerId, busId, validity):
        self.ticketId = ticketId
        self.passengerId = passengerId
        self.busId = busId
        self.validity = validity
    
    def verifyTicket(self):
        return self.validity

class BusTerminal:
    def __init__(self, terminalId, location):
        self.terminalId = terminalId
        self.location = location
    
    def verifyTicket(self, ticket):
        return ticket.verifyTicket()
    
    def managePassengerFlow(self):
        print("Managing passenger flow at the terminal.")

class Bus:
    def __init__(self, busId, capacity, currentLocation):
        self.busId = busId
        self.capacity = capacity
        self.currentLocation = currentLocation
        self.passengers = []
    
    def updateLocation(self, newLocation):
        self.currentLocation = newLocation
    
    def communicateWithControlSystem(self, control_system):
        control_system.receiveBusLocation(self.busId, self.currentLocation)
    
    def boardPassenger(self, ticket):
        if len(self.passengers) < self.capacity and ticket.busId == self.busId:
            self.passengers.append(ticket.passengerId)
            return True
        return False
    
    def alightPassenger(self, passengerId):
        if passengerId in self.passengers:
            self.passengers.remove(passengerId)

class CentralizedControlSystem:
    def __init__(self, systemId):
        self.systemId = systemId
        self.busLocations = {}
    
    def manageSchedule(self):
        print("Managing bus schedule.")
    
    def provideRouteInfo(self):
        print("Providing route information.")
    
    def monitorTraffic(self):
        print("Monitoring traffic conditions.")
    
    def receiveBusLocation(self, busId, location):
        self.busLocations[busId] = location
        print(f"Bus {busId} is currently at {location}.")

# Example usage:
passenger1 = Passenger(1, "John Doe", "john@example.com")
passenger2 = Passenger(2, "Jane Smith", "jane@example.com")
payment_app = PaymentApp(1, "EZPay")
bus_terminal = BusTerminal(1, "Main Terminal")
bus = Bus(101, 2, "Main Terminal")
control_system = CentralizedControlSystem(1)

ticket1 = passenger1.purchaseTicket(payment_app, bus.busId)
ticket2 = passenger2.purchaseTicket(payment_app, bus.busId)

passenger1.boardBus(ticket1, bus_terminal)
bus.boardPassenger(ticket1)
passenger2.boardBus(ticket2, bus_terminal)
bus.boardPassenger(ticket2)

bus.updateLocation("Next Stop")
bus.communicateWithControlSystem(control_system)
passenger1.alightBus(bus)
passenger2.alightBus(bus)
