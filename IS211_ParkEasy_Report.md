# IS-211 Mandatory Assignment — Spring 2026
## ParkEasy: A City Parking Management System

**Group members:** [Member 1], [Member 2], [Member 3], [Member 4]
**Course:** IS-211 — Information Systems
**Submission date:** [Date]

---

## Table of Contents
1. Business Idea Description
2. Application Features
3. Analysis of Python Code
4. Data Structures
5. References

---

## 1. Business Idea Description (Mats)

### The Idea
**ParkEasy** is a city-operated digital parking management system designed to help citizens find, reserve, and manage parking spots in real time. The system is owned and operated by the municipality, functioning as a public digital service — similar to public transportation apps or online citizen portals.

### The Problem It Solves
Urban parking is a persistent challenge in Norwegian and European cities. Drivers often spend significant time circling city blocks looking for available spots, contributing to traffic congestion, increased emissions, and frustration. Traditional parking systems offer no real-time visibility into spot availability, making efficient use of public parking infrastructure difficult.

ParkEasy addresses this by providing:
- Real-time availability of all municipal parking spots
- Digital reservations so citizens can guarantee a spot before driving
- A fair waitlist system to manage demand when the lot is full
- Accessible parking management with support for disabled and electric-vehicle spots

### Target Users
- **Citizens** who need to park in the city centre
- **City administrators** who manage lot capacity, maintenance, and allocation
- **Accessibility services** requiring reliable disabled parking management

### Public Sector Justification
As a public sector initiative, ParkEasy aligns with municipal obligations to provide efficient infrastructure to citizens. A city-run system avoids profit-driven pricing and ensures equitable access. It can be integrated with existing city apps, smart city platforms, and traffic management systems. Funding would come from municipal budgets or EU smart city grants, with optional pay-per-use fees to cover operational costs.

---

## 2. Application Features (Hans Kristian)

The prototype is implemented in Python and demonstrates the core logic of the system. A production version would include a web or mobile frontend, a database backend, and integration with payment and traffic systems.

### 2.1 Core Classes

#### ParkingSpot
Represents a single physical parking spot. Each spot holds:
- `spot_id` — unique identifier (e.g. "A-01")
- `location` — human-readable location (e.g. "Level 1 - North")
- `spot_type` — category: "standard", "disabled", or "electric"
- `is_available` — boolean availability flag
- `reserved_by` — the name/ID of the citizen holding the spot

```python
class ParkingSpot:
    def __init__(self, spot_id: str, location: str, spot_type: str = "standard"):
        self.spot_id = spot_id
        self.location = location
        self.spot_type = spot_type
        self.is_available = True
        self.reserved_by = None
```

#### ParkEasy
The main system class that manages all spots and the waitlist. It exposes the following key methods:

| Method | Description | Time Complexity |
|---|---|---|
| add_spot(id, location, type) | Register a new parking spot | O(1) |
| remove_spot(id) | Remove a spot (e.g. maintenance) | O(1) |
| reserve_spot(id, citizen) | Reserve a specific spot by ID | O(1) |
| release_spot(id) | Free a spot and auto-assign to waitlist | O(1) |
| find_available_spots(type) | Scan all spots for availability | O(n) |
| get_spot(id) | Direct lookup of a spot | O(1) |
| join_waitlist(citizen) | Add citizen to FIFO waitlist | O(1) |
| leave_waitlist(citizen) | Remove citizen from waitlist | O(n) |
| lot_status() | Summary report of lot usage | O(n) |

### 2.2 Key Functions Explained

#### reserve_spot — O(1) Direct Reservation
```python
def reserve_spot(self, spot_id: str, citizen: str) -> bool:
    if spot_id not in self.spots:       # O(1) hash lookup
        return False
    spot = self.spots[spot_id]          # O(1) hash access
    if not spot.is_available:
        return False
    spot.is_available = False
    spot.reserved_by = citizen
    return True
```
This function uses Python's built-in dictionary (hash table) for direct O(1) access by spot_id. No loop or comparison is needed — the hash function maps the ID directly to the object in memory.

#### release_spot — O(1) Release with Auto-Assign
```python
def release_spot(self, spot_id: str) -> None:
    spot = self.spots[spot_id]              # O(1)
    spot.is_available = True
    spot.reserved_by = None
    if self.waitlist:
        next_citizen = self.waitlist.popleft()  # O(1) dequeue
        self.reserve_spot(spot_id, next_citizen)
```
When a spot is freed, the system immediately checks the queue. If someone is waiting, popleft() from the deque runs in O(1) and the spot is re-assigned automatically.

#### find_available_spots — O(n) Linear Scan
```python
def find_available_spots(self, spot_type: str = None) -> list:
    available = []
    for spot in self.spots.values():    # O(n) — visits every spot
        if spot.is_available:
            if spot_type is None or spot.spot_type == spot_type:
                available.append(spot)
    return available
```
This function must visit every spot once to check availability. There is no shortcut — we cannot know which spots are available without inspecting each one. This is an O(n) operation where n is the number of spots in the system.

---

## 3. Analysis of Python Code (Kristian)

The application demonstrates three distinct time complexity classes.

### 3.1 O(1) — Constant Time

**Where:** add_spot, remove_spot, reserve_spot, release_spot, get_spot, join_waitlist

**Why O(1)?**
Python dictionaries are implemented as hash tables. When a key (e.g. "A-01") is passed, Python computes a hash value and maps it directly to a memory location. This does NOT depend on how many spots exist in the system — whether there are 10 or 10,000 spots, the lookup takes the same constant time.

```python
# O(1) — regardless of how many spots are in the system
spot = self.spots["A-01"]
```

Similarly, Python's collections.deque is a doubly-linked list that supports O(1) appends and pops from both ends:

```python
self.waitlist.append(citizen)           # O(1)
next_citizen = self.waitlist.popleft()  # O(1)
```

For a real-world city system handling thousands of transactions per day, O(1) operations are critical for performance and responsiveness.

### 3.2 O(n) — Linear Time

**Where:** find_available_spots, lot_status, print_all_spots, leave_waitlist

**Why O(n)?**
When the system must examine every spot (e.g. to find all available ones), it must iterate over all n items. The time taken grows linearly with the number of spots.

```python
for spot in self.spots.values():   # visits all n spots
    if spot.is_available:
        available.append(spot)
```

This cannot be reduced to O(1) without maintaining a separate index of available spots, which would add memory overhead and complexity to every reservation and release operation. O(n) scans are acceptable for batch operations like generating reports or listing available spots.

### 3.3 Complexity Summary Table

| Operation | Complexity | Reason |
|---|---|---|
| Reserve a spot by ID | O(1) | Hash table direct access |
| Release a spot | O(1) | Hash table + deque popleft |
| Add/remove a spot | O(1) | Hash table insert/delete |
| Direct spot lookup | O(1) | Hash table get |
| Join waitlist | O(1) | Deque append |
| Find all available spots | O(n) | Must visit every spot |
| Generate lot status report | O(n) | Must count all spots |
| Leave waitlist by name | O(n) | Sequential scan of queue |

---

## 4. Data Structures (Kasper)

The application uses two primary data structures covered in IS-211.

### 4.1 Hash Table (Python dict)

**Used in:** self.spots — the central registry of all parking spots

**What it is:**
A hash table maps keys to values using a hash function. Each key is passed through the hash function to compute an index (bucket) where the value is stored. On average, lookup, insertion, and deletion all run in O(1).

**How it is used:**
```python
self.spots: dict[str, ParkingSpot] = {}

# Insert — O(1)
self.spots[spot_id] = ParkingSpot(spot_id, location, spot_type)

# Lookup — O(1)
spot = self.spots[spot_id]

# Delete — O(1)
del self.spots[spot_id]

# Membership check — O(1)
if spot_id in self.spots:
    ...
```

**Why this data structure?**
Parking spots are naturally identified by a unique ID. A hash table is the optimal structure when the primary access pattern is direct lookup by key. The O(1) performance is far superior to alternatives:

| Structure | Lookup | Why not chosen |
|---|---|---|
| Unsorted list | O(n) | Too slow for direct lookup |
| Sorted list | O(log n) | Slower; harder to maintain |
| Hash table | O(1) | Best for key-based access |

### 4.2 Queue (Python collections.deque)

**Used in:** self.waitlist — the FIFO waiting list of citizens

**What it is:**
A queue is a First-In-First-Out (FIFO) data structure. Items are added at the back (enqueue) and removed from the front (dequeue). Python's deque supports O(1) operations at both ends, making it ideal for queue use cases.

**How it is used:**
```python
from collections import deque
self.waitlist: deque[str] = deque()

# Enqueue — citizen joins the back of the line — O(1)
self.waitlist.append(citizen)

# Dequeue — first citizen gets the next available spot — O(1)
next_citizen = self.waitlist.popleft()
```

**Why this data structure?**
A queue enforces FIFO fairness — the first citizen to join the waitlist gets the next available spot. This is both fair and intuitive for a public service. A regular Python list could simulate a queue, but list.pop(0) is O(n) because all remaining elements must shift left. The deque avoids this with its doubly-linked structure.

| Structure | Dequeue from front | Why not chosen |
|---|---|---|
| Python list | O(n) | All elements shift on pop(0) |
| deque (chosen) | O(1) | Optimised for both ends |
| Stack | O(1) | LIFO — unfair order |

---

## 5. References

- Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2013). *Data Structures and Algorithms in Python*. Wiley.
- Python Documentation. (2024). *collections.deque*. https://docs.python.org/3/library/collections.html
- Python Documentation. (2024). *Mapping Types — dict*. https://docs.python.org/3/library/stdtypes.html
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.

---

*AI tools used during prototyping: Claude (Anthropic) was used to help structure and generate the initial prototype code. All code was reviewed, understood, and adapted by all group members before inclusion in this report.*
