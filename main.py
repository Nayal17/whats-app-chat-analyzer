import streamlit as st
import preprocess
import analyzer
import plotly.express as px

st.set_page_config(layout="wide")
st.sidebar.title('Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.provider(data)
    # st.dataframe(df)

    df = df[df['users']!='group_notification']
    users = df['users'].unique().tolist()
    users.sort()
    users.insert(0,'Overall Analysis')

    opted_user = st.sidebar.selectbox('User Analysis',users)

    word_cloud = analyzer.word_cloud(opted_user,df)

    fig = px.imshow(word_cloud)  
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        autosize=False,
        width=1400,
        height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")

    if st.sidebar.button('Show Analysis'):
        col1, col2, col3, col4 = st.columns(4)
        count = analyzer.stats(opted_user,df)

        with col1:
            st.header('Total messages')
            st.title(count['msg_count'])

        with col2:
            st.header('Total Words')
            st.title(count['word_count'])

        with col3:
            st.header('Media Shared')
            st.title(count['media_count'])

        with col4:
            st.header('URL Shared')
            st.title(count['url_count'])
        st.markdown("""---""")
        
        st.title('Monthly Timeline')
        timeline = analyzer.m_timeline(opted_user,df)
        fig = px.line(timeline,x='time',y='messages')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""---""")

        st.title('Daily Timeline')
        timeline = analyzer.d_timeline(opted_user,df)
        fig = px.line(timeline,x='the_date',y='messages')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""---""")

        st.title('Weekly Status')
        status = analyzer.weekly_activity(opted_user,df)
        fig = px.line(x=status.index ,y=status )
        fig.update_layout(xaxis_title='Day', yaxis_title='Number of messages',font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="LightGreen"
                ))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""---""")

        if opted_user=='Overall Analysis':
            col1, col2 = st.columns((2,1))
            active_data, active_users = analyzer.top_charts(df)
            with col1:
                st.title('Most active users')
                fig = px.bar(y=active_users.index,x=active_users)
                fig.update_layout(xaxis_title='Messages Count', yaxis_title='Top 5 Users',font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="LightGreen"
                ))
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.title('Active status')
                st.dataframe(active_data)
                st.markdown("""---""")

        
        st.title('Most common words')
        common_words = analyzer.common_words(opted_user,df)
        fig = px.bar(x=common_words.Word,y=common_words.Frequency)
        fig.update_layout(yaxis_title='Frequency', xaxis_title='Top 10 words',font=dict(
            family="Courier New, monospace",
            size=18,
            color="LightGreen"
        ))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""---""")
        emoji_df = analyzer.common_emoji(opted_user,df)

        col1,col2 = st.columns((1,4))
        with col1:
            st.title('Emojis')
            st.dataframe(emoji_df)
        with col2:
            fig = px.pie(emoji_df, values='Frequency', names='Emoji',color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            fig.update_layout(yaxis_title='Frequency', xaxis_title='Most common Emojis',font=dict(
                family="Courier New, monospace",
                size=18,
                color="LightGreen"
            ))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("""---""")
        
        