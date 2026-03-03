"""
ParkEasy - City Parking Management System
IS-211 Mandatory Assignment | Spring 2026
Group of 4 | Public Sector Business
"""

from collections import deque


# ─────────────────────────────────────────
#  DATA STRUCTURES USED:
#   1. Hash Table (dict)  → O(1) spot lookup / reserve / release
#   2. Queue (deque)      → O(1) waitlist enqueue / dequeue
#   3. List (array)       → O(n) scan for available spots
# ─────────────────────────────────────────


class ParkingSpot:
    """Represents a single parking spot in the city lot."""

    def __init__(self, spot_id: str, location: str, spot_type: str = "standard"):
        self.spot_id = spot_id          # e.g. "A-01"
        self.location = location        # e.g. "Level 1 - North Wing"
        self.spot_type = spot_type      # "standard", "disabled", "electric"
        self.is_available = True
        self.reserved_by = None         # citizen name or ID

    def __repr__(self):
        status = "Available" if self.is_available else f"Reserved by {self.reserved_by}"
        return f"[{self.spot_id}] {self.location} ({self.spot_type}) → {status}"


class ParkEasy:
    """
    City Parking Management System.

    Data Structures:
    ─────────────────────────────────────────────────────────────────
    1. Hash Table (self.spots: dict)
       - Key: spot_id (string), Value: ParkingSpot object
       - Used for O(1) average-case lookup, reservation, and release
       - Ideal for direct access by known spot ID (city map integration)

    2. Queue (self.waitlist: deque)
       - FIFO queue of citizen names waiting for a free spot
       - enqueue (append) and dequeue (popleft) both run in O(1)
       - Ensures fair, first-come-first-served waitlist management

    3. List / Array (self.spots.values())
       - Used when scanning ALL spots to find available ones
       - Sequential scan → O(n) time complexity
       - Acceptable trade-off since full scans are less frequent
    ─────────────────────────────────────────────────────────────────
    """

    def __init__(self):
        # DATA STRUCTURE 1: Hash Table
        # Dictionary maps spot_id → ParkingSpot
        # Average O(1) insert, lookup, delete
        self.spots: dict[str, ParkingSpot] = {}

        # DATA STRUCTURE 2: Queue
        # Waitlist for citizens when lot is full
        # O(1) enqueue / dequeue
        self.waitlist: deque[str] = deque()

    # ── Spot Management ────────────────────────────────────────────

    def add_spot(self, spot_id: str, location: str, spot_type: str = "standard") -> None:
        """
        Add a new parking spot to the system.
        Time Complexity: O(1) — hash table insertion
        """
        if spot_id in self.spots:
            print(f"  ⚠ Spot '{spot_id}' already exists.")
            return
        self.spots[spot_id] = ParkingSpot(spot_id, location, spot_type)
        print(f"  ✓ Spot '{spot_id}' added at {location}.")

    def remove_spot(self, spot_id: str) -> None:
        """
        Remove a spot from the system (e.g. under maintenance).
        Time Complexity: O(1) — hash table deletion
        """
        if spot_id not in self.spots:
            print(f"  ✗ Spot '{spot_id}' not found.")
            return
        del self.spots[spot_id]
        print(f"  ✓ Spot '{spot_id}' removed from system.")

    # ── Reservation ────────────────────────────────────────────────

    def reserve_spot(self, spot_id: str, citizen: str) -> bool:
        """
        Reserve a specific spot by its ID.
        Time Complexity: O(1) — direct hash table lookup by key
        """
        if spot_id not in self.spots:                  # O(1) lookup
            print(f"  ✗ Spot '{spot_id}' does not exist.")
            return False

        spot = self.spots[spot_id]                     # O(1) access

        if not spot.is_available:
            print(f"  ✗ Spot '{spot_id}' is already taken.")
            return False

        spot.is_available = False
        spot.reserved_by = citizen
        print(f"  ✓ Spot '{spot_id}' reserved for {citizen}.")
        return True

    def release_spot(self, spot_id: str) -> None:
        """
        Free a spot and automatically assign it to the next person
        in the waitlist (if any).
        Time Complexity:
          - O(1) for hash lookup and waitlist dequeue
          - O(1) overall
        """
        if spot_id not in self.spots:                  # O(1)
            print(f"  ✗ Spot '{spot_id}' not found.")
            return

        spot = self.spots[spot_id]                     # O(1)
        prev = spot.reserved_by
        spot.is_available = True
        spot.reserved_by = None
        print(f"  ✓ Spot '{spot_id}' released (was held by {prev}).")

        # Auto-assign to next person in waitlist
        if self.waitlist:
            next_citizen = self.waitlist.popleft()     # O(1) dequeue
            self.reserve_spot(spot_id, next_citizen)
            print(f"  → Auto-assigned to '{next_citizen}' from waitlist.")

    # ── Availability Search ─────────────────────────────────────────

    def find_available_spots(self, spot_type: str = None) -> list[ParkingSpot]:
        """
        Find all available spots, optionally filtered by type.
        Time Complexity: O(n) — must iterate through all n spots
        This is unavoidable when no index on 'is_available' exists.
        """
        available = []
        for spot in self.spots.values():               # O(n) scan
            if spot.is_available:
                if spot_type is None or spot.spot_type == spot_type:
                    available.append(spot)
        return available

    def get_spot(self, spot_id: str) -> ParkingSpot | None:
        """
        Get details of a specific spot.
        Time Complexity: O(1) — hash table lookup
        """
        return self.spots.get(spot_id)                 # O(1)

    # ── Waitlist ────────────────────────────────────────────────────

    def join_waitlist(self, citizen: str) -> None:
        """
        Add a citizen to the waitlist when the lot is full.
        Time Complexity: O(1) — deque append
        """
        self.waitlist.append(citizen)                  # O(1)
        position = len(self.waitlist)
        print(f"  ✓ {citizen} added to waitlist. Position: #{position}.")

    def leave_waitlist(self, citizen: str) -> None:
        """
        Remove a citizen from the waitlist (cancelled request).
        Time Complexity: O(n) — must scan queue to find the citizen
        Queues are not optimised for random removal.
        """
        if citizen in self.waitlist:                   # O(n) scan
            self.waitlist.remove(citizen)              # O(n) removal
            print(f"  ✓ {citizen} removed from waitlist.")
        else:
            print(f"  ✗ {citizen} not found in waitlist.")

    # ── Reporting ───────────────────────────────────────────────────

    def lot_status(self) -> None:
        """
        Print a summary of the parking lot status.
        Time Complexity: O(n) — iterates all spots once
        """
        total = len(self.spots)
        available = sum(1 for s in self.spots.values() if s.is_available)  # O(n)
        occupied = total - available

        print("\n" + "=" * 50)
        print("  ParkEasy — City Parking Lot Status")
        print("=" * 50)
        print(f"  Total spots   : {total}")
        print(f"  Available     : {available}")
        print(f"  Occupied      : {occupied}")
        print(f"  Waitlist size : {len(self.waitlist)}")
        print("=" * 50)

    def print_all_spots(self) -> None:
        """
        Display all spots and their status.
        Time Complexity: O(n)
        """
        print("\n  All Parking Spots:")
        print("  " + "-" * 46)
        for spot in self.spots.values():               # O(n)
            print(f"  {spot}")
        print()


# ─────────────────────────────────────────
#  DEMO / TEST RUN
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("\n🚗 ParkEasy — City Parking Management System\n")

    system = ParkEasy()

    # Add spots — O(1) each
    print("── Adding Spots ──────────────────────────────")
    system.add_spot("A-01", "Level 1 - North", "standard")
    system.add_spot("A-02", "Level 1 - North", "standard")
    system.add_spot("A-03", "Level 1 - North", "disabled")
    system.add_spot("B-01", "Level 2 - South", "electric")
    system.add_spot("B-02", "Level 2 - South", "standard")

    # Reserve spots — O(1) each
    print("\n── Reserving Spots ───────────────────────────")
    system.reserve_spot("A-01", "Lars Hansen")
    system.reserve_spot("A-02", "Mia Olsen")
    system.reserve_spot("B-01", "Jonas Berg")
    system.reserve_spot("B-02", "Sara Dahl")
    system.reserve_spot("A-03", "Elias Vik")

    # Show status — O(n)
    system.lot_status()

    # Search for available spots — O(n)
    print("\n── Searching Available Spots ─────────────────")
    available = system.find_available_spots()
    if available:
        for s in available:
            print(f"  {s}")
    else:
        print("  No spots available — lot is full.")

    # Add to waitlist — O(1) each
    print("\n── Joining Waitlist ──────────────────────────")
    system.join_waitlist("Nora Lie")
    system.join_waitlist("Erik Strand")

    # Release a spot — O(1), triggers auto-assign from queue
    print("\n── Releasing a Spot ──────────────────────────")
    system.release_spot("A-02")

    # Search for disabled spots — O(n)
    print("\n── Finding Disabled Spots ────────────────────")
    disabled = system.find_available_spots(spot_type="disabled")
    for s in disabled:
        print(f"  {s}")

    # Direct lookup — O(1)
    print("\n── Direct Spot Lookup (O(1)) ─────────────────")
    spot = system.get_spot("B-01")
    print(f"  {spot}")

    # Final status
    system.lot_status()
    system.print_all_spots()
