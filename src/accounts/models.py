from datetime import datetime
from typing import Optional
import re
from sqlalchemy import String, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from src.models import Base



class User(Base):
	__tablename__ = "user_account"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)

	username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
	first_name: Mapped[str] = mapped_column(String(30), nullable=True)
	last_name: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
	password: Mapped[str] = mapped_column(String(128))
	email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)

	is_staff: Mapped[bool] = mapped_column(default=False, nullable=False)
	is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
	is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)

	# groups: Mapped[List["Group"]] = relationship("Group", secondary="user_group", back_populates="users")
	last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
	date_joined: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=False ,default=func.now())

	def get_full_name(self) -> str:
		"""
		Return the first_name plus the last_name, with a space in between.
		"""
		full_name = "%s %s" % (self.first_name, self.last_name)
		return full_name.strip()

	@validates('username')
	def validate_username(self, key, username):
		if not re.match(r'^[\w.@+-]+\Z', username):
			raise ValueError("Username may contain only letters, digits and @/./+/-/_ characters.")
		if len(username) > 150:
			raise ValueError("Username must be 150 characters or fewer.")
		return username

	@validates('email')
	def validate_email(self, key, email):
		if email and len(email) > 254:
			raise ValueError("Email must be 254 characters or fewer.")
		return email

	def __repr__(self) -> str:
		return f"User(id={self.id!r}, username={self.username!r}, fullname={self.get_full_name()!r})"







