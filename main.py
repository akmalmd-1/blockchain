from enum import Enum
import time

class Status(Enum):
    Created = 0
    Packed = 1
    InTransit = 2
    Delivered = 3
    Sold = 4
    Recalled = 5

class History:
    def __init__(self, timestamp, updater, status, location, note):
        self.timestamp = timestamp
        self.updater = updater
        self.status = status
        self.location = location
        self.note = note

class Product:
    def __init__(self, pid, name, description, owner):
        self.id = pid
        self.name = name
        self.description = description
        self.currentOwner = owner
        self.status = Status.Created
        self.history = []

class SupplyChain:
    def __init__(self):
        self.products = {}
        self.nextId = 1

    def createProduct(self, name, description, location, owner="User"):
        pid = self.nextId
        self.nextId += 1
        p = Product(pid, name, description, owner)
        p.history.append(History(time.time(), owner, p.status, location, "Created"))
        self.products[pid] = p
        print(f"✅ ProductCreated: ID={pid}, Name={name}, Owner={owner}")
        return pid

    def updateStatus(self, pid, newStatus, newOwner=None, location="", note="", updater="User"):
        if pid not in self.products:
            raise Exception("Product not found")
        p = self.products[pid]
        p.status = newStatus
        if newOwner:
            p.currentOwner = newOwner
        p.history.append(History(time.time(), updater, newStatus, location, note))
        print(f"🚚 StatusUpdated: ID={pid}, Status={newStatus.name}, Updater={updater}")

    def getProduct(self, pid):
        p = self.products[pid]
        return (p.name, p.description, p.currentOwner, p.status, len(p.history))

    def getHistory(self, pid, index):
        p = self.products[pid]
        h = p.history[index]
        return (h.timestamp, h.updater, h.status, h.location, h.note)

# --- Example usage ---
if __name__ == "__main__":
    sc = SupplyChain()
    pid = sc.createProduct("Widget-123", "Blue gadget", "Factory A", owner="Alice")
    sc.updateStatus(pid, Status.InTransit, newOwner="Bob", location="Truck 12", note="In transit", updater="Alice")

    product = sc.getProduct(pid)
    print("ℹ Product:", product)

    for i in range(product[4]):
        print("History", i, sc.getHistory(pid, i))
