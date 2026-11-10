import os

import requests
import streamlit as st

API_URL = os.getenv("NOTES_API_URL", "http://localhost:5000/api").rstrip("/")

st.set_page_config(page_title="Notes", page_icon="📝")

if "token" not in st.session_state:
    st.session_state.token = None


def api(method, path, payload=None):
    """Send a request to the API and return its data or an error message."""
    headers = {}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    try:
        response = requests.request(
            method,
            API_URL + path,
            json=payload,
            headers=headers,
            timeout=10,
        )
    except requests.exceptions.ConnectionError:
        return None, (
            f"Cannot reach the backend at {API_URL}. Start it in a separate terminal "
            "from the backend folder with `npm start`. If this frontend is hosted "
            "remotely, set NOTES_API_URL to the backend's reachable API URL; "
            "localhost refers to the host running Streamlit."
        )
    except requests.exceptions.Timeout:
        return None, f"The backend at {API_URL} did not respond within 10 seconds."
    except requests.exceptions.RequestException as exc:
        return None, f"The request to {API_URL} failed: {exc}"

    try:
        data = response.json()
    except ValueError:
        data = {}
    if response.ok:
        return data, None

    if response.status_code == 401:
        st.session_state.token = None
    return None, data.get("error", {}).get("message", "Something went wrong.")


def auth_page():
    st.title("📝 Notes")
    login_tab, signup_tab = st.tabs(["Log in", "Sign up"])

    with login_tab:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pw")
        if st.button("Log in"):
            data, err = api("POST", "/auth/login", {"email": email, "password": password})
            if err:
                st.error(err)
            else:
                st.session_state.token = data["token"]
                st.rerun()

    with signup_tab:
        name = st.text_input("Name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password (min 8 characters)", type="password", key="signup_pw")
        if st.button("Sign up"):
            data, err = api("POST", "/auth/signup", {"name": name, "email": email, "password": password})
            if err:
                st.error(err)
            else:
                st.session_state.token = data["token"]
                st.rerun()


def notes_page():
    st.title("📝 My Notes")
    if st.button("Log out"):
        st.session_state.token = None
        st.rerun()

    st.subheader("New note")
    title = st.text_input("Title", key="new_title")
    content = st.text_area("Content", key="new_content")
    if st.button("Add note"):
        _, err = api("POST", "/notes", {"title": title, "content": content})
        if err:
            st.error(err)
        else:
            st.session_state.pop("new_title", None)
            st.session_state.pop("new_content", None)
            st.rerun()

    st.subheader("Your notes")
    data, err = api("GET", "/notes")
    if err:
        st.error(err)
        return

    notes = data["notes"]
    if not notes:
        st.info("No notes yet.")

    for note in notes:
        with st.expander(note["title"]):
            new_title = st.text_input("Title", note["title"], key=f"t{note['id']}")
            new_content = st.text_area("Content", note["content"], key=f"c{note['id']}")
            col1, col2 = st.columns(2)
            if col1.button("Update", key=f"u{note['id']}"):
                _, err = api("PUT", f"/notes/{note['id']}", {"title": new_title, "content": new_content})
                if err:
                    st.error(err)
                else:
                    st.rerun()
            if col2.button("Delete", key=f"d{note['id']}"):
                api("DELETE", f"/notes/{note['id']}")
                st.rerun()


if st.session_state.token:
    notes_page()
else:
    auth_page()
