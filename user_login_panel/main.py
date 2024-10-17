import streamlit as st
from controllers.user_controller import UserController

def main():
    user_controller = UserController()
    user_view = user_controller.handle_main_page()

    if user_controller.get_logged_in():
        sidebar = user_view.get_sidebar()

        # Adicionando mais componentes diretamente
        with sidebar:
            st.write(f"Data Inicial: {user_view.get_start_date()}")
            st.write(f"Data Final: {user_view.get_end_date()}")
        
        st.write(user_controller.get_permition())
        st.write(user_controller.get_exception())
        
# Execução do programa
if __name__ == "__main__":
    main()