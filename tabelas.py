from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime, ForeignKey, join, select, insert, update
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

from config import get_engine


Base = declarative_base()
Session = sessionmaker(bind=get_engine())
session = Session()

class cadastroprodutos(Base):
    __tablename__="cadastroprodutos"
    __table_args__ = {"schema": "Produtos"}
    idcadastro = Column(Integer, primary_key=True)
    idpreco = Column(Integer)
    urljet = Column(String, unique=False, nullable=False)
    categoriashausz = Column(String, unique=False, nullable=False)
    categorias = Column(String, unique=False, nullable=False)
    sku = Column(String, unique=False, nullable=False)
    ean =Column(String, unique=False, nullable=False)
    marca = Column(String, unique=False, nullable=False)
    nomeproduto = Column(String, unique=False, nullable=False)
    descricao = Column(String, unique=False, nullable=False)
    imagens = Column(String, unique=False, nullable=False)
    atributos = Column(String, unique=False, nullable=False)
    skuhausz = Column(String, unique=False, nullable=False)
    nomeprodutohausz =Column(String, unique=False, nullable=False)
    urlproduto =Column(String, unique=False, nullable=False)
    origem =Column(String, unique=False, nullable=False)
    bitcompativel = Column(Boolean, unique=False, nullable=False)
    datacadastrado = Column(DateTime, unique=False, nullable=False)
    idurlbase = Column(Integer)
