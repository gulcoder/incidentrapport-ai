from pydantic import BaseModel, field_validator

class IncidentReport(BaseModel):
    Sammanfattning: str
    Kategori: str
    Prioritet: str

    @field_validator('Kategori')
    def validate_kategori(cls, value):
        tillåtna = {"nätverk", "programvara", "hårdvara"}
        if value not in tillåtna:
            raise ValueError(f"Kategori måste vara en av {tillåtna}.")
        return value

    @field_validator('Prioritet')
    def validate_prioritet(cls, value):
        tillåtna = {"Låg", "Medel", "Hög", "Kritisk"}
        if value not in tillåtna:
            raise ValueError(f"Prioritet måste vara en av {tillåtna}.")
        return value

