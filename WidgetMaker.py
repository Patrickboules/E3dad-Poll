from DataLoading import *

def create_custom_topic_input():
    selected = (st.session_state.form['is_custom_selected'] and 
               st.session_state.form['custom_topic'].strip())
    
    container_class = "custom-topic-container"
    if selected:
        container_class += " custom-topic-selected"
    
    st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
    st.markdown("<h2 class='header'> أو اكتب موضوعًا مخصصًا من عندك: </h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_input(
            "موضوع مخصص",
            value=st.session_state.form['custom_topic'],
            key="custom_topic_input",
            label_visibility="collapsed",
            placeholder="اكتب موضوعًا مخصصًا إذا لم تجد ما تبحث عنه",
        )
    with col2:
        if st.button("اختر", key="select_custom", use_container_width=True):
            handle_custom_topic()
    
    st.markdown('</div>', unsafe_allow_html=True)


def handle_custom_topic():
    """Handle custom topic input and selection"""
    # Clear any predefined selection
    if st.session_state.form['selected_option'] is not None:
        prev_option = st.session_state.form['selected_option']
        st.session_state.form['temp_counts'][prev_option] = st.session_state.form['temp_counts'].get(prev_option, 0) - 1
        st.session_state.form['selected_option'] = None
    
    # Update custom topic state
    custom_text = st.session_state.custom_topic_input.strip()
    st.session_state.form['custom_topic'] = custom_text
    st.session_state.form['is_custom_selected'] = bool(custom_text)
    save_response()
    st.rerun()

def create_option(num, text, user_selections,limit):
    combined_counts = get_combined_counts()
    count = combined_counts.get(num, 0)
    max_limit = limit
    progress = (count / max_limit) * 100
    
    # Check if user has already selected this topic (max 3 per phone)
    phone = st.session_state.form['phone_number']
    user_topics = user_selections.get(phone, [])
    user_topic_count = user_topics.count(num)
    disabled = count >= max_limit or user_topic_count >= 3
    
    # Determine if this option is selected
    selected = (st.session_state.form['selected_option'] == num and 
               not st.session_state.form['is_custom_selected'])
    
    container = st.container()
    container.markdown(
        f"""
        <div class="option-container {'selected' if selected else ''} {'disabled' if disabled and not selected else ''}" 
             id="option_{num}"
             onclick="handleClick({num})">
            <div class="option-header">
                <div class="option-number">{num}.</div>
                <div class="count-display">({count}/{max_limit}) - اختياراتك:</div>
            </div>
            <div class="option-text">{text}</div>
            <div class="progress-container">
                <div class="progress-bar {'complete' if count >= max_limit else ''}" style="width:{progress}%"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = container.columns([1, 1])
    
    # Select button (only enabled if not disabled)
    if not disabled:
        if col1.button("اختر", key=f"select_{num}"):
            handle_option_selection(num)
    
    # Deselect button (only shown if this option is selected)
    if selected:
        if col2.button("إلغاء الاختيار", key=f"deselect_{num}"):
            handle_deselection(num)
    else:
        # Empty space to maintain layout
        col2.empty()


def handle_deselection(option_num):
    """Handle deselection of an option"""
    if st.session_state.form['selected_option'] == option_num:
        # Update counts for the deselected option
        st.session_state.form['temp_counts'][option_num] = st.session_state.form['temp_counts'].get(option_num, 0) - 1
        st.session_state.form['selected_option'] = None
        save_response()
        st.rerun()


def handle_option_selection(option_num):
    """Handle selection of a predefined option"""
    # Clear any custom selection
    st.session_state.form['custom_topic'] = ''
    st.session_state.custom_topic_input = ''
    st.session_state.form['is_custom_selected'] = False
    
    # Update counts for previous selection if exists
    if st.session_state.form['selected_option'] is not None:
        prev_option = st.session_state.form['selected_option']
        st.session_state.form['temp_counts'][prev_option] = st.session_state.form['temp_counts'].get(prev_option, 0) - 1
    
    # Set new selection
    st.session_state.form['selected_option'] = option_num
    st.session_state.form['temp_counts'][option_num] = st.session_state.form['temp_counts'].get(option_num, 0) + 1
    save_response()
    st.rerun()
