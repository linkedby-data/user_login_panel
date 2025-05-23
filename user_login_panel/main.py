import sys
import os
import streamlit as st

# Adicionando o caminho do diretório do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from user_login_panel.controllers.user_controller import UserController
from user_login_panel.utils.session_manager import SessionManager

# Configuração da página deve ser o primeiro comando Streamlit
st.set_page_config(page_title="User Login Panel", layout="wide")

def main():
    # Inicializa o gerenciador de sessão
    SessionManager.get_session_id()

    user_controller = UserController()
    user_view = user_controller.handle_main_page()

    if user_controller.get_logged_in():
        sidebar = user_view.get_sidebar()

        # Adicionando mais componentes diretamente
        with sidebar:
            st.write(f"Data Inicial: {user_view.get_start_date()}")
            st.write(f"Data Final: {user_view.get_end_date()}")
        
        st.write(user_controller.get_permission())
        st.write(user_controller.get_exception())
        
# Execução do programa
if __name__ == "__main__":
    main()