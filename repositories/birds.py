from fastapi import HTTPException, status
from sqlmodel import Session, select
from models.birds import Bird, BirdCreate
from models.species import Species

class BirdRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(Bird)
        birds = self.session.exec(statement).all()
        return birds
    
    def insert(self, payload: BirdCreate):
        species = self.session.get(Species, payload.species_id)
        if species is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Species with id {payload.species_id} does not exist",
            )

        bird = Bird.model_validate(payload)
        self.session.add(bird)
        self.session.commit()
        self.session.refresh(bird)
        return bird
