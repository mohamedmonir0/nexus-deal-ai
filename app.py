import streamlit as st
import os
import time
import pandas as pd
import plotly.graph_objects as go
import graphviz
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from duckduckgo_search import DDGS

# 1. Load Environment
load_dotenv()

# 2. Page Config
st.set_page_config(page_title="NEXUS DEAL AI", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 🎨 UI HACKS (Clean minimal look)
# ==========================================
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; max-width: 95%;}
    hr {margin-top: 0.5rem; margin-bottom: 0.5rem; border-color: #1f2937;}
    </style>
""", unsafe_allow_html=True)

# TOP HEADER
c_head1, c_head2 = st.columns([3, 1])
with c_head1:
    st.markdown("<h3 style='color: #58A6FF;'>💠 NEXUS DEAL AI | VENDOR PROPOSAL ANALYSIS</h3>", unsafe_allow_html=True)
with c_head2:
    st.markdown("<div style='text-align: right; color: #00ffaa; margin-top: 15px;'>Status: Ready for Execution 🟢</div>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 🎛️ MAIN LAYOUT (3 COLUMNS)
# ==========================================
col_left, col_mid, col_right = st.columns([1, 1.6, 1.2], gap="large")

with col_left:
    st.markdown("<h4 style='color: #C9D1D9;'>VENDOR PROPOSAL</h4>", unsafe_allow_html=True)
    supp_a_name = st.text_input("Vendor A", value="AWS")
    supp_a_cost = st.number_input(f"{supp_a_name} Base Cost ($)", value=50000, step=1000)
    supp_a_uptime = st.number_input(f"{supp_a_name} Uptime (%)", value=99.9, step=0.01)
    
    st.markdown("<br>", unsafe_allow_html=True)
    supp_b_name = st.text_input("Vendor B", value="Azure")
    supp_b_cost = st.number_input(f"{supp_b_name} Base Cost ($)", value=65000, step=1000)
    supp_b_uptime = st.number_input(f"{supp_b_name} Uptime (%)", value=99.99, step=0.01)
    
    st.markdown("<br>", unsafe_allow_html=True)
    downtime_cost = st.number_input("Downtime Impact ($/hr)", value=5000, step=500)
    
    st.markdown("<br>", unsafe_allow_html=True)
    execute_btn = st.button("🚀 INITIATE AI ANALYSIS", use_container_width=True, type="primary")

# Variables
tco_a, tco_b, savings, winner = 0, 0, 0, "N/A"
risk_score_a, risk_score_b = 0, 0
executive_summary = ""
negotiation_email = ""

# ==========================================
# 🧠 EXECUTION BLOCK & ANIMATION
# ==========================================
if execute_btn:
    with col_mid:
        anim_box = st.empty()
        with anim_box.status("🧠 **Initiating Multi-Agent Swarm...**", expanded=True) as status:
            time.sleep(0.5)
            st.write("🌍 **System:** Securely pulling live market data...")
            
            # Deterministic Search
            try:
                with DDGS() as ddgs:
                    live_data_a = str([r for r in ddgs.text(f"{supp_a_name} cloud outage data breach", max_results=1)])
                    live_data_b = str([r for r in ddgs.text(f"{supp_b_name} cloud outage data breach", max_results=1)])
            except:
                live_data_a, live_data_b = "Nominal", "Nominal"
            market_context = f"Intel:\n{supp_a_name}: {live_data_a}\n{supp_b_name}: {live_data_b}"
            
            time.sleep(1)
            st.write("🕵️‍♂️ **Agent 1 (Researcher):** Analyzing market vulnerabilities...")
            time.sleep(1)
            st.write("🧮 **Agent 2 (Analyst):** Processing Total Cost of Ownership (TCO)...")
            time.sleep(1)
            st.write("💼 **Agent 3 (Negotiator):** Synthesizing Executive Summary...")
            time.sleep(1)
            st.write("🥷 **Agent 4 (The Closer):** Drafting vendor negotiation protocol...")
            
            # Math
            downtime_hrs_a = 8760 * (1 - supp_a_uptime / 100)
            tco_a = supp_a_cost + (downtime_hrs_a * downtime_cost)
            risk_score_a = min(100, max(0, int((downtime_hrs_a / 10) * 100))) 
            
            downtime_hrs_b = 8760 * (1 - supp_b_uptime / 100)
            tco_b = supp_b_cost + (downtime_hrs_b * downtime_cost)
            risk_score_b = min(100, max(0, int((downtime_hrs_b / 10) * 100)))
            
            savings = abs(tco_a - tco_b)
            winner = supp_a_name if tco_a < tco_b else supp_b_name
            loser = supp_b_name if winner == supp_a_name else supp_a_name

            # CrewAI (4 Agents)
            groq_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
            
            researcher = Agent(role='Intelligence Analyst', goal='Assess risk.', backstory='Data-driven.', verbose=False, allow_delegation=False, llm=groq_llm)
            analyst = Agent(role='Financial Quant', goal='Calculate TCO.', backstory='Math genius.', verbose=False, allow_delegation=False, llm=groq_llm)
            negotiator = Agent(role='Chief Negotiator', goal='Write executive summary.', backstory='Corporate executive.', verbose=False, allow_delegation=False, llm=groq_llm)
            closer = Agent(role='The Closer', goal='Write negotiation email.', backstory='Ruthless corporate negotiator.', verbose=False, allow_delegation=False, llm=groq_llm)
            
            task1 = Task(description=f'Summarize risks based on: {market_context}', expected_output='Risk summary.', agent=researcher)
            task2 = Task(description=f'Calculate TCO for {supp_a_name} vs {supp_b_name}.', expected_output='Math output.', agent=analyst)
            task3 = Task(description=f'Write a 1-paragraph executive decision. The winner is {winner}. State the savings of ${savings:,.0f}.', expected_output='Executive summary.', agent=negotiator)
            task4 = Task(description=f'Write a firm email to the LOSING vendor ({loser}). State they lost due to high TCO and downtime risks. Give them ONE chance to drastically cut their base price.', expected_output='Corporate email.', agent=closer)
            
            deal_crew = Crew(agents=[researcher, analyst, negotiator, closer], tasks=[task1, task2, task3, task4], process=Process.sequential)
            deal_crew.kickoff()
            
            executive_summary = task3.output.raw
            negotiation_email = task4.output.raw
            
            status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
            time.sleep(0.5)
        anim_box.empty() # Hide the animation box to keep UI clean after finishing

# ==========================================
# 📊 MIDDLE COLUMN: ARCHITECTURE, SUMMARY & EMAIL
# ==========================================
with col_mid:
    st.markdown("#### Multi-Agent Architecture (CrewAI)")
    
    # 1. GRAPHVIZ: 4 Agents drawn cleanly
    graph = graphviz.Digraph(engine='dot')
    graph.attr(bgcolor='transparent', color='white', fontcolor='white', rankdir='TD')
    
    # Nodes with Emojis and clear names
    graph.node('A', '🕵️‍♂️\nMarket\nResearcher', shape='circle', color='#00f0ff', fontcolor='white', penwidth='2')
    graph.node('B', '🧮\nFinancial\nAnalyst', shape='circle', color='#ff416c', fontcolor='white', penwidth='2')
    graph.node('C', '💼\nChief\nNegotiator', shape='circle', color='#00ffaa', fontcolor='white', penwidth='2')
    graph.node('D', '🥷\nThe\nCloser', shape='circle', color='#ffb703', fontcolor='white', penwidth='2')
    
    # Edges
    graph.edge('A', 'C', color='#58A6FF')
    graph.edge('B', 'C', color='#58A6FF')
    graph.edge('C', 'D', color='#58A6FF')
    
    st.graphviz_chart(graph)
    
    if execute_btn:
        st.markdown("#### Executive Summary")
        st.info(executive_summary)

        st.markdown("#### TCO Breakdown")
        m1, m2 = st.columns(2)
        m1.metric(label=f"{supp_a_name} TCO", value=f"${tco_a:,.0f}", delta=f"-${(tco_a - supp_a_cost):,.0f} Risk", delta_color="inverse")
        m2.metric(label=f"{supp_b_name} TCO", value=f"${tco_b:,.0f}", delta=f"-${(tco_b - supp_b_cost):,.0f} Risk", delta_color="inverse")

        st.markdown("---")
        st.markdown("#### 💣 Auto-Negotiation Protocol (The Closer)")
        st.markdown(f"""
        <div style="background-color: #161b22; border-left: 4px solid #ffb703; padding: 15px; border-radius: 5px;">
            <strong style="color: #ffb703;">TO: {supp_a_name if winner == supp_b_name else supp_b_name} Sales Division</strong><br><br>
            <span style="color: #c9d1d9; font-family: monospace; font-size: 0.95rem;">{negotiation_email.replace(chr(10), '<br>')}</span>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 📈 RIGHT COLUMN: CHARTS & VISUALS (PLOTLY)
# ==========================================
with col_right:
    st.markdown("#### RECOMMENDATION")
    if execute_btn:
        st.markdown(f"<h3 style='color: #00ffaa;'>CHOOSE {winner.upper()}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #00f0ff;'>Projected Savings: ${savings:,.0f} / Year</p>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color: #58A6FF;'>AWAITING DATA</h3>", unsafe_allow_html=True)
    
    st.markdown("---")

    if execute_btn:
        # 1. BAR CHART (5-Year Savings)
        st.markdown("##### 5-Year Savings Projection")
        years = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
        proj_savings = [savings, savings*2, savings*3, savings*4, savings*5]
        fig_bar = go.Figure(data=[go.Bar(x=years, y=proj_savings, marker_color='#00f0ff')])
        fig_bar.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#C9D1D9'))
        st.plotly_chart(fig_bar, use_container_width=True)

        # 2. DONUT CHART (TCO Components)
        st.markdown("##### TCO Breakdown")
        fig_pie = go.Figure(data=[go.Pie(labels=['Base Cost', 'Risk/Downtime Cost'], values=[supp_a_cost if winner == supp_a_name else supp_b_cost, (tco_a - supp_a_cost) if winner == supp_a_name else (tco_b - supp_b_cost)], hole=.6, marker_colors=['#58A6FF', '#ff416c'])])
        fig_pie.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#C9D1D9'), showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

        # 3. GAUGE CHARTS (Vendor Risk Index)
        st.markdown("##### Vendor Risk Index")
        g1, g2 = st.columns(2)
        with g1:
            fig_g1 = go.Figure(go.Indicator(mode="gauge+number", value=risk_score_a, title={'text': supp_a_name, 'font': {'size': 14}}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#ff416c"}}))
            fig_g1.update_layout(height=150, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#C9D1D9'))
            st.plotly_chart(fig_g1, use_container_width=True)
        with g2:
            fig_g2 = go.Figure(go.Indicator(mode="gauge+number", value=risk_score_b, title={'text': supp_b_name, 'font': {'size': 14}}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#00ffaa"}}))
            fig_g2.update_layout(height=150, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#C9D1D9'))
            st.plotly_chart(fig_g2, use_container_width=True)
