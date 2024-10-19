import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import hashlib
import re
from user_login_panel.config.database import get_db_url

Base = declarative_base()

class User(Base):
    __tablename__ = f"users_{st.secrets.MISCELLANEOUS.subject}"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    enterprise = Column(String, nullable=False)
    position = Column(String, nullable=False)
    permition = Column(String, nullable=False)
    exception = Column(String, nullable=False)
    autorization = Column(String, nullable=False)
    password = Column(String, nullable=False)

class UserModel:
    def __init__(self):
        self.engine = create_engine(get_db_url())
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_email(self, email):
        session = self.Session()
        
        try:
            return session.query(User).filter_by(email=email).first() is not None
        finally:
            session.close()

    def check_login(self, email, password):
        session = self.Session()
        
        try:
            hashed_password = self.hash_password(password)
            return session.query(User).filter_by(email=email, password=hashed_password).first() 
        finally:
            session.close()

    def register_user(self, inserted_data):
        session = self.Session()
        hashed_password = self.hash_password(inserted_data["new_password"])
        
        try:
            if session.query(User).filter_by(email=inserted_data["new_email"]).first():
                return False  # Usuário já cadastrado

            new_user = User(
                email=inserted_data["new_email"],
                name=inserted_data["new_name"],
                enterprise=inserted_data["new_enterprise"],
                position=inserted_data["new_position"],
                permition=inserted_data["new_permition"],
                exception=inserted_data["new_exception"],
                autorization=inserted_data["autorization_code"],
                password=hashed_password
            )
            
            session.add(new_user)
            session.commit()            
            return True  # Usuário cadastrado com sucesso
        finally:
            session.close()
    '''
    def update_user(self, email, updated_data):
        session = self.Session()
        
        try:
            st.write(updated_data)
            st.write(f"Updating user: {email}")
            
            # Monta a query de UPDATE diretamente
            update_query = (
                session.query(User)
                .filter_by(email=email)
                .update({
                    User.name: updated_data.get("new_name"),
                    User.enterprise: updated_data.get("new_enterprise"),
                    User.position: updated_data.get("new_position"),
                    User.permition: updated_data.get("new_permition"),
                    User.exception: updated_data.get("new_exception"),
                    User.autorization: updated_data.get("new_autorization"),
                    User.password: self.hash_password(updated_data["password"]) if "password" in updated_data else None
                }, synchronize_session=False)
            )
            
            if update_query:
                session.commit()
                st.write("User updated successfully")
                return True
            
            st.write(f"User with email {email} not found.")
            return False
        except Exception as e:
            st.write(f"Error updating user: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    '''
    '''
    def update_user(self, email, updated_data):
        session = self.Session()
        
        try:
            # Verifica se o usuário existe
            user_exists = session.query(User).filter_by(email=email).first()
            
            if user_exists:
                # Cria um dicionário com os dados a serem atualizados
                update_fields = {
                    "name": updated_data.get("name", user_exists.name),
                    "enterprise": updated_data.get("enterprise", user_exists.enterprise),
                    "position": updated_data.get("position", user_exists.position),
                    "permition": updated_data.get("permition", user_exists.permition),
                    "exception": updated_data.get("exception", user_exists.exception),
                    "autorization": updated_data.get("autorization", user_exists.autorization),
                }
                
                # Verifica se a senha está sendo atualizada
                if "password" in updated_data:
                    update_fields["password"] = self.hash_password(updated_data["password"])

                # Executa a atualização no banco
                session.query(User).filter_by(email=email).update(update_fields)

                # Faz o commit para persistir as alterações
                session.commit()
                return True
            else:
                st.write(f"User with email {email} not found.")
                return False
        except Exception as e:
            st.write(f"Error updating user: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    '''

    '''
    def update_user(self, email, updated_data):
        session = self.Session()
        
        try:
            user = session.query(User).filter_by(email=email).first()
            
            if user:
                st.write(f"Updating user: {email} with data: {updated_data}")
                st.write(f"Session is active: {session.is_active}")  # Verifique se a sessão está ativa

                user.name = updated_data.get("name", user.name)
                user.enterprise = updated_data.get("enterprise", user.enterprise)
                user.position = updated_data.get("position", user.position)
                user.permition = updated_data.get("permition", user.permition)
                user.exception = updated_data.get("exception", user.exception)
                user.autorization = updated_data.get("autorization", user.autorization)
                
                if "password" in updated_data:
                    user.password = self.hash_password(updated_data["password"])
                
                session.commit()
                st.write("Commit executed")  # Confirme o commit

                session.refresh(user)  # Garante que as alterações sejam visíveis na sessão
                st.write(f"Updated user: {user}")  # Mostra os dados atualizados
                return True
            
            st.write(f"User with email {email} not found.")
            return False
        except Exception as e:
            st.write(f"Error updating user: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    '''

    '''
    def update_user(self, email, updated_data):
        session = self.Session()
        
        try:
            user = session.query(User).filter_by(email=email).first()
            
            if user:
                st.write(f"Updating user: {email} with data: {updated_data}")  # Adicione logs para inspecionar os dados
                user.name = updated_data.get("name", user.name)
                user.enterprise = updated_data.get("enterprise", user.enterprise)
                user.position = updated_data.get("position", user.position)
                user.permition = updated_data.get("permition", user.permition)
                user.exception = updated_data.get("exception", user.exception)
                user.autorization = updated_data.get("autorization", user.autorization)
                
                if "password" in updated_data:
                    user.password = self.hash_password(updated_data["password"])
                
                session.commit()
                session.refresh(user)  # Garante que a sessão está atualizada após o commit
                st.write("User updated successfully.")  # Log de sucesso
                return True
            
            st.write(f"User with email {email} not found.")  # Log de falha
            return False
        except Exception as e:
            st.write(f"Error updating user: {e}")  # Adiciona logging de erro
            session.rollback()  # Reverte alterações em caso de erro
            return False
        finally:
            session.close()
    '''
    
    
    def update_user(self, email, updated_data):
        session = self.Session()
        
        try:
            user = session.query(User).filter_by(email=email).first()
            
            if user:
                user.name = updated_data.get("new_name", user.name)
                user.enterprise = updated_data.get("new_enterprise", user.enterprise)
                user.position = updated_data.get("new_position", user.position)
                user.permition = updated_data.get("new_permition", user.permition)
                user.exception = updated_data.get("new_exception", user.exception)
                user.autorization = updated_data.get("autorization_code", user.autorization)
                
                if "new_password" in updated_data:
                    user.password = self.hash_password(updated_data["new_password"])
                
                session.commit()                
                return True
            
            return False
        finally:
            session.close()
    

    def delete_user(self, email):
        session = self.Session()
        
        try:
            user = session.query(User).filter_by(email=email).first()
            
            if user:
                session.delete(user)
                session.commit()                
                return True
            
            return False
        finally:
            session.close()

    @staticmethod
    def is_valid_email(email):
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(regex, email)