import streamlit as st
import pandas as pd

# Initialize book data
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["Title", "Author", "Genre", "Year", "Status"])

# Load existing data or initialize
if "library_data" not in st.session_state:
    st.session_state.library_data = load_data()

# Application title
st.title("📚 Automatic Library Management System")

menu = st.sidebar.radio(
    "Menu",
    ["Add Book",'View Book','Search book','checkout/return book']
)

if menu == "Add Book":
    st.header("Add a New Book to the library")
    with st.form("add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        genre = st.selectbox("Genre",
         ['Fiction','Non-fiction','Science','Biography','Other']
                             )
        year = st.number_input("Year of publication", min_value=1000, max_value=2100, step=1,value=2025)
        submit_button = st.form_submit_button("Add Book")

        if submit_button:
          if title and author:
              new_book = {"Title": title, "Author": author, "Genre": genre, "Year": year, "Status": "Available"}
              st.session_state.library_data = pd.concat([st.session_state.library_data, pd.DataFrame([new_book])], ignore_index=True)
              st.success(f"Book '{title}' by {author} has been added to the library!")
          else:
              st.error("Please enter a valid title and author.")

#view all books
elif menu == "View Book":
    st.header("Library Books")
    st.dataframe(st.session_state.library_data)

#search books
elif menu == "Search book":
    st.header("Search for Books")
    # Search for books by title or author
    search_option= st.radio("Search by",['Title','Author'])
    search_term = st.text_input(f"Enter {search_option}:")
    submit_button = st.button("Search")
    if submit_button and search_term:
        filtered_date = st.session_state.library_data[
            st.session_state.libarary_data[search_option].str.constains(search_term,case=False,na=False)
        ]
        if not filtered_date.empty:
            st.dataframe(filtered_date)
        else:
            st.warning(f"No books found for {search_option}: {search_term}'.")

#check out/return a book
elif menu == "Check Out/Return Book":
  st.header("Manage Book Status")
  with st.form('manage_status_form'):
    book_title = st.text_input("Enter Book Title")
    action = st.selectbox("Action",['Check Out','Return'])
    submit = st.form_submit_button("Update Status")
    if submit:
      if book_title:
        book_index = st.session_state.library_data[
        st.session_state.library_data['Title'].str.contains(book_title, case=False, na=False)].index
        if not book_index.empty:
          current_status = st.session_state.library_data.at[book_index[0], 'Status']
          if action == 'Check Out' and current_status == 'Available':
            st.session_state.library_data.at[book_index[0], 'Status'] = 'Checked Out'
            st.success(f"Book '{book_title}' has been checked out.")
          elif action == 'Return' and current_status == 'Checked Out':
            st.session_state.library_data.at[book_index[0], 'Status'] = 'Available'
            st.success(f"Book '{book_title}' has been returned.")
          else:
            st.error(f"Cannot perform action. Current status: {current_status}")
        else:
          st.error("Book not found. Please check the title and try again.")
      else:
        st.error("Please enter a book title.")
