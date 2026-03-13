from fastapi import HTTPException, status
from sqlmodel import Session, select
from models.birds import Bird
from models.birdspotting import Birdspotting, BirdspottingCreate


class BirdspottingRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(Birdspotting)
        return self.session.exec(statement).all()

    def get_one(self, spotting_id: int):
        item = self.session.get(Birdspotting, spotting_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Birdspotting with id {spotting_id} does not exist",
            )
        return item

    def insert(self, payload: BirdspottingCreate):
        bird = self.session.get(Bird, payload.bird_id)
        if bird is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bird with id {payload.bird_id} does not exist",
            )
        item = Birdspotting.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item
