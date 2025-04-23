import streamlit as st
import uuid
import time
from typing import Any, Dict, Optional
from threading import Lock

class SessionManager:
    # Dicionário global para armazenar todas as sessões
    _sessions: Dict[str, Dict[str, Any]] = {}
    # Dicionário para armazenar o último acesso de cada sessão
    _last_access: Dict[str, float] = {}
    # Tempo de expiração da sessão em segundos (1 hora)
    SESSION_TIMEOUT = 3600
    # Lock para operações thread-safe
    _lock = Lock()

    @classmethod
    def _cleanup_expired_sessions(cls) -> None:
        """Remove sessões expiradas."""
        current_time = time.time()
        expired_sessions = [
            session_id for session_id, last_access in cls._last_access.items()
            if current_time - last_access > cls.SESSION_TIMEOUT
        ]
        
        with cls._lock:
            for session_id in expired_sessions:
                cls._sessions.pop(session_id, None)
                cls._last_access.pop(session_id, None)

    @classmethod
    def _update_last_access(cls, session_id: str) -> None:
        """Atualiza o timestamp do último acesso da sessão."""
        with cls._lock:
            cls._last_access[session_id] = time.time()

    @classmethod
    def get_session_id(cls) -> str:
        """Obtém ou cria um ID de sessão único para a aba atual."""
        # Limpa sessões expiradas antes de criar/obter uma nova
        cls._cleanup_expired_sessions()

        if "session_id" not in st.session_state:
            if "session_id" in st.query_params:
                session_id = st.query_params["session_id"]
            else:
                session_id = str(uuid.uuid4())
                st.query_params["session_id"] = session_id
            st.session_state["session_id"] = session_id
            
            # Inicializa o estado da sessão se não existir
            with cls._lock:
                if session_id not in cls._sessions:
                    cls._sessions[session_id] = {}
                    cls._last_access[session_id] = time.time()
        
        # Atualiza o timestamp do último acesso
        cls._update_last_access(st.session_state["session_id"])
        return st.session_state["session_id"]

    @classmethod
    def get_session_state(cls, key: str, default: Any = None) -> Any:
        """Obtém um valor do estado da sessão atual."""
        session_id = cls.get_session_id()
        with cls._lock:
            if session_id not in cls._sessions:
                cls._sessions[session_id] = {}
            return cls._sessions[session_id].get(key, default)

    @classmethod
    def set_session_state(cls, key: str, value: Any) -> None:
        """Define um valor no estado da sessão atual."""
        session_id = cls.get_session_id()
        with cls._lock:
            if session_id not in cls._sessions:
                cls._sessions[session_id] = {}
            cls._sessions[session_id][key] = value
            cls._last_access[session_id] = time.time()

    @classmethod
    def clear_session(cls) -> None:
        """Limpa o estado da sessão atual."""
        session_id = cls.get_session_id()
        with cls._lock:
            if session_id in cls._sessions:
                cls._sessions[session_id] = {}
                cls._last_access[session_id] = time.time()

    @classmethod
    def get_all_sessions(cls) -> Dict[str, Dict[str, Any]]:
        """Retorna uma cópia de todas as sessões ativas."""
        cls._cleanup_expired_sessions()
        with cls._lock:
            return cls._sessions.copy()

    @classmethod
    def get_session_count(cls) -> int:
        """Retorna o número de sessões ativas."""
        cls._cleanup_expired_sessions()
        with cls._lock:
            return len(cls._sessions) 