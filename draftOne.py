class Passenger:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
    
    def purchaseTicket(self, payment_app):
        if payment_app.processPayment():
            return payment_app.generateTicket(self.id)
        return None
    
    def boardBus(self, ticket, bus_terminal):
        if bus_terminal.verifyTicket(ticket):
            print(f"Passenger {self.name} boarded the bus.")
        else:
            print(f"Passenger {self.name} could not board the bus due to invalid ticket.")
    
    def alightBus(self):
        print(f"Passenger {self.name} alighted the bus.")

class PaymentApp:
    def __init__(self, appId, appName):
        self.appId = appId
        self.appName = appName
    
    def processPayment(self):
        # Simulate payment processing
        return True
    
    def generateTicket(self, passengerId):
        # Simulate ticket generation
        return Ticket(1, passengerId, 101, True)

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
    
    def updateLocation(self, newLocation):
        self.currentLocation = newLocation
    
    def communicateWithControlSystem(self, control_system):
        control_system.receiveBusLocation(self.busId, self.currentLocation)

class CentralizedControlSystem:
    def __init__(self, systemId):
        self.systemId = systemId
    
    def manageSchedule(self):
        print("Managing bus schedule.")
    
    def provideRouteInfo(self):
        print("Providing route information.")
    
    def monitorTraffic(self):
        print("Monitoring traffic conditions.")
    
    def receiveBusLocation(self, busId, location):
        print(f"Bus {busId} is currently at {location}.")

# Example usage:
passenger = Passenger(1, "John Doe", "john@example.com")
payment_app = PaymentApp(1, "EZPay")
bus_terminal = BusTerminal(1, "Main Terminal")
bus = Bus(101, 50, "Main Terminal")
control_system = CentralizedControlSystem(1)

ticket = passenger.purchaseTicket(payment_app)
passenger.boardBus(ticket, bus_terminal)
bus.updateLocation("Next Stop")
bus.communicateWithControlSystem(control_system)
passenger.alightBus()
