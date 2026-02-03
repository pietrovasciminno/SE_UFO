from dataclasses import dataclass

@dataclass
class State:
    id: str
    name: str
    lat: float
    lng: float


    def __str__(self):
        return f"{self.id}: {self.name} "


    def __hash__(self):
        return hash(self.id)