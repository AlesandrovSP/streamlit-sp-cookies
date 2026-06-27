import os
import streamlit as st
import streamlit.components.v1 as components

_FRONTEND = os.path.join(os.path.dirname(os.path.realpath(__file__)), "frontend")
_func     = components.declare_component("sp_cookie_manager", path=_FRONTEND)
_KEY      = "_sp_cm_state"


class CookieManager:
    """
    Persistent cookie manager for Streamlit.
    Resuelve el problema de persistencia de streamlit-cookies-controller:
    - Archivos en site-packages (no 404)
    - Una sola instancia via key fijo (no conflictos entre páginas)
    - Lee con st.context.cookies (síncrono, sin iframe issues)
    - Escribe con el componente (allow-same-origin sandbox)

    Uso en app.py:
        cm      = CookieManager()
        cookies = cm.get_all()
        if cookies is None:
            st.stop()  # primer render, browser aún no respondió
        val = cookies.get("mi_cookie")
        cm.set("mi_cookie", "valor", days=7)
        cm.delete("mi_cookie")
    """

    def get_all(self) -> dict | None:
        pending = st.session_state.pop("_sp_cm_pending", None)

        if pending:
            result = _func(
                action  = pending["action"],
                name    = pending.get("name"),
                value   = pending.get("value", ""),
                max_age = pending.get("max_age", 604800),
                key     = _KEY,
                default = None,
            )
        else:
            result = _func(
                action  = "read",
                key     = _KEY,
                default = None,
            )

        if result is None:
            return None
        return result.get("cookies", {})

    def set(self, name: str, value: str, days: int = 7) -> None:
        st.session_state["_sp_cm_pending"] = {
            "action" : "write",
            "name"   : name,
            "value"  : value,
            "max_age": days * 86400,
        }

    def delete(self, name: str) -> None:
        st.session_state["_sp_cm_pending"] = {
            "action": "delete",
            "name"  : name,
        }
