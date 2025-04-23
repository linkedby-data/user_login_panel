import streamlit as st
from datetime import datetime
from user_login_panel.utils.session_manager import SessionManager

class UserViewHelper:
    def __init__(self):
        # Verifica se a chave 'current_page' existe no session_state, caso contrário, cria.
        if "current_page" not in st.session_state:
            st.session_state.current_page = "login"
    
    def set_logo(self, image_path):
        """
        Define o logotipo no aplicativo Streamlit.
        :param image_path: Caminho da imagem do logotipo.
        """
        st.image(image_path)
    
    def set_title(self, title):
        """
        Define o título da página Streamlit.
        :param title: O título da página.
        """
        st.title(title)

    def show_message(self, message, level="info"):
        """
        Exibe uma mensagem no aplicativo com diferentes níveis (info, success, warning, error).
        :param message: Mensagem a ser exibida.
        :param level: Nível da mensagem (info, success, warning, error). Default é 'info'.
        """
        if level == "success":
            st.success(message)
        elif level == "warning":
            st.warning(message)
        elif level == "error":
            st.error(message)
        else:
            st.info(message)

    def set_page(self, page, refresh=False):
        """
        Define a página atual no session_state.
        :param page: O nome ou identificador da página.
        """
        st.session_state.current_page = page
        SessionManager.set_session_state("current_page", page)
        
        if refresh:
            st.rerun()  # Atualiza a página

    def get_page(self):
        return st.session_state.current_page

class UserViewRegisterAndLogin:
    def login_page(self):
        st.subheader("Login ou Cadastro")
        return st.tabs(["Login", "Cadastrar"])

    def login_form(self):
        session_id = SessionManager.get_session_id()
        email = st.text_input("Email", key=f"{session_id}_login_user")
        password = st.text_input("Senha", type="password", key=f"{session_id}_login_pass")
        return email, password

    def register_form(self):
        session_id = SessionManager.get_session_id()
        new_email = st.text_input("Novo Email", key=f"{session_id}_register_user")
        new_name = st.text_input("Nome", key=f"{session_id}_username")
        new_enterprise = st.text_input("Empresa", key=f"{session_id}_user_enterprise")
        new_position = st.text_input("Cargo", key=f"{session_id}_user_position")
        new_permission = st.text_input("Permissão", key=f"{session_id}_user_permission")
        new_exception = st.text_input("Exceção", key=f"{session_id}_user_exception")
        autorization_code = st.text_input("Código de Autorização", type="password", key=f"{session_id}_register_code")
        new_password = st.text_input("Nova Senha", type="password", key=f"{session_id}_register_pass")
        confirm_password = st.text_input("Confirme a Senha", type="password", key=f"{session_id}_confirm_pass")

        return {
            "new_email": new_email,
            "new_name": new_name,
            "new_enterprise": new_enterprise,
            "new_position": new_position,
            "new_permission": new_permission,
            "new_exception": new_exception,
            "autorization_code": autorization_code,
            "new_password": new_password,
            "confirm_password": confirm_password
        }

    def display_action_buttons(self):
        session_id = SessionManager.get_session_id()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            register_button = st.button("Cadastrar", key=f"{session_id}_register_button", use_container_width=True)
        
        with col2:
            update_button = st.button("Alterar", key=f"{session_id}_update_button", use_container_width=True)
        
        with col3:
            delete_button = st.button("Excluir", key=f"{session_id}_delete_button", use_container_width=True)

        return register_button, update_button, delete_button

class UserViewSidebar:
    _users: dict = {}
    
    def __init__(self):
        self.sidebar = st.sidebar
        self.search_button = None
        self.logout_button = None
        self.start_date = None
        self.end_date = None

    def set_user(self, user):
        session_id = SessionManager.get_session_id()
        self._users[session_id] = user
    
    def get_user(self):
        session_id = SessionManager.get_session_id()
        return self._users.get(session_id)
    
    def display(self):
        with self.sidebar:
            self.sidebar.subheader(f"Bem-vindo, {self.get_user()}!")

            col1, col2 = st.columns(2)
        
            with col1:
                self.refresh_button = st.button("Atualizar", key=f"{SessionManager.get_session_id()}_refresh_button", use_container_width=True)
            
            with col2:
                self.logout_button = st.button("Logout", key=f"{SessionManager.get_session_id()}_logout_button", use_container_width=True)

            self.start_date = self.sidebar.date_input(
                "Data Inicial",
                value=datetime.now(),
                min_value=datetime(2024, 1, 1),
                max_value=datetime(2050, 12, 31),
                format="DD/MM/YYYY",
                key=f"{SessionManager.get_session_id()}_start_date"
            )

            self.end_date = self.sidebar.date_input(
                "Data Final",
                value=datetime.now(),
                min_value=self.start_date,
                max_value=datetime(2030, 12, 31),
                format="DD/MM/YYYY",
                key=f"{SessionManager.get_session_id()}_end_date"
            )
    
    def get_sidebar(self):
        return self.sidebar
    
    def get_refresh_button(self):
        return self.refresh_button
    
    def get_logout_button(self):
        return self.logout_button
    
    def get_start_date(self):
        return self.start_date
    
    def get_end_date(self):
        return self.end_date