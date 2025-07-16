from DataLoading import *
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
def create_option(num, data, user_selections):
    text, max_limit,leaders = data  # Unpack the tuple
    combined_counts = get_combined_counts()
    count = combined_counts.get(num, 0)
    progress = (count / max_limit) * 100
    
    phone = st.session_state.form['phone_number']
    user_topics = user_selections.get(phone, [])
    user_topic_count = user_topics.count(num)
    disabled = count >= max_limit or user_topic_count >= max_limit
    
    selected = (st.session_state.form['selected_option'] == num and 
               not st.session_state.form['is_custom_selected'])
    
    container = st.container()
    container.markdown(
    f"""
    <div class="option-container {'selected' if selected else ''} {'disabled' if disabled and not selected else ''}" 
         onclick="handleClick({num})">
        <div class="option-header">
            <span class="option-number">{num}.</span>
            <span class="counts">({count}/{max_limit})</span>
            <span class="leaders">{leaders}</span>
        </div>
        <div class="option-text">{text}</div>
        <div class="progress-container">
            <div class="progress-bar" style="width:{progress}%"></div>
        </div>
        {f'<div class="full-badge">FULL</div>' if count >= max_limit else ''}
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

def option_click_js():
    return """
    <script>
    function handleClick(optionNum) {
        const buttons = parent.document.querySelectorAll('button[title="اختر"]');
        buttons.forEach(button => {
            if (button.textContent.includes("اختر") && 
                button.getAttribute("data-testid").includes(optionNum)) {
                button.click();
            }
        });
    }

    function enforceLightMode() {
        document.documentElement.style.backgroundColor = '#ffffff';
        document.documentElement.style.colorScheme = 'light';
        document.body.style.backgroundColor = '#ffffff';
        document.body.classList.remove('dark');

        const darkModeToggle = document.querySelector('[data-testid="stToolbar"]');
        if (darkModeToggle) darkModeToggle.style.display = 'none';
    }

    // Initial call and interval check
    window.addEventListener('load', enforceLightMode);
    setInterval(enforceLightMode, 500);
    </script>
    """

def get_combined_counts():
    existing_data = load_responses()
    topic_counts, _ = process_responses(existing_data)
    
    # Combine with temporary selections
    combined = topic_counts.copy()
    for num, count in st.session_state.form['temp_counts'].items():
        combined[num] += count
    return combined