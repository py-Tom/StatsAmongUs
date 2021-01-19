import re
import ast
import plotly.graph_objects as go


def get_name(user):
    pattern = re.compile(r"#\d{4}$")
    match = re.search(pattern, user).span()
    user_name = user[: match[0]]
    user_id = user[match[0] :]
    temp_ = (user_name, user_id)
    return temp_


def graph_sankey(
    user_name,
    games_start,
    games_finished,
    total_crew,
    total_impo,
    impo_vote,
    impo_kill,
    impo_sab,
    crew_vote,
    crew_task,
):
    won_crew = crew_vote + crew_task
    won_impo = impo_vote + impo_kill + impo_sab
    lost_crew = total_crew - won_crew
    lost_impo = total_impo - won_impo
    disconnects = (games_start - games_finished) / games_start * 100
    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=60,
                    thickness=15,
                    label=[
                        f"Total: {games_start}",
                        f"Crewmate: {total_crew}",
                        f"Impostor: {total_impo}",
                        f"Lost: {lost_crew}",
                        f"Won: {won_crew}",
                        f"Won: {won_impo}",
                        f"Lost: {lost_impo}",
                        f"Vote: {crew_vote}",
                        f"Task: {crew_task}",
                        f"Kill: {impo_kill}",
                        f"Vote: {impo_vote}",
                        f"Sabotage: {impo_sab}",
                    ],
                    x=[0.01, 0.33, 0.33, 0.66, 0.66, 0.66, 0.66, 1, 1, 1, 1, 1],
                    y=[0.5, 0.4, 0.6, 0.2, 0.3, 0.5, 0.6, 0.2, 0.2, 0.8, 0.8, 0.8],
                    color=[
                        "rgba(228, 224, 220, 0.5)",
                        "rgba(183, 221, 176, 0.5)",
                        "rgba(249, 172, 187, 0.5)",
                        "rgba(63, 111, 33, 0.5)",
                        "rgba(97, 189, 79, 0.5)",
                        "rgba(238,105,105, 0.5)",
                        "rgba(244,193,193, 0.5)",
                        "rgba(96, 168, 10, 0.5)",
                        "rgba(116, 201, 12, 0.5)",
                        "rgba(242, 37, 37, 0.5)",
                        "rgba(191, 28, 28, 0.5)",
                        "rgba(168, 28, 28, 0.5)",
                    ],
                ),
                link=dict(
                    source=[0, 0, 1, 1, 2, 2, 4, 4, 5, 5, 5],
                    target=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                    value=[
                        total_crew,
                        total_impo,
                        lost_crew,
                        won_crew,
                        won_impo,
                        lost_impo,
                        crew_vote,
                        crew_task,
                        impo_kill,
                        impo_vote,
                        impo_sab,
                    ],
                    color=[
                        "rgba(183, 221, 176, 0.7)",
                        "rgba(249, 172, 187, 0.7)",
                        "rgba(63, 111, 33, 0.7)",
                        "rgba(97, 189, 79, 0.7)",
                        "rgba(238,105,105, 0.7)",
                        "rgba(244,193,193, 0.7)",
                        "rgba(96, 168, 10, 0.7)",
                        "rgba(116, 201, 12, 0.7)",
                        "rgba(242, 37, 37, 0.7)",
                        "rgba(191, 28, 28, 0.7)",
                        "rgba(168, 28, 28, 0.7)",
                    ],
                ),
            )
        ]
    )
    fig.add_annotation(
        x=0.01,
        y=0.01,
        text=f"disconnects = {round(disconnects, 2)}%",
        font_size=10,
        showarrow=False,
    )
    fig.update_layout(title_text=f"Statistics: <b>{user_name}", font_size=12)
    fig.update_layout(autosize=False, width=750, height=500)
    #  fig.show()
    fig.write_image(f"temp/fig_sankey_{user_name}.png")


def graph_winratio(
    user_name,
    total_crew,
    total_impo,
    impo_vote,
    impo_kill,
    impo_sab,
    crew_vote,
    crew_task,
):
    crew_p = round((crew_vote + crew_task) / total_crew * 100, 1)
    impo_p = round((impo_vote + impo_kill + impo_sab) / total_impo * 100, 1)
    crew_v = round(crew_vote / total_crew * 100, 1)
    crew_t = round(crew_task / total_crew * 100, 1)
    impo_v = round(impo_vote / total_impo * 100, 1)
    impo_s = round(impo_sab / total_impo * 100, 1)
    impo_k = round(impo_kill / total_impo * 100, 1)

    role = [f"Crewmate<br>WinRate: {crew_p}%", f"Impostor<br>WinRate: {impo_p}%"]

    fig = go.Figure(
        data=[
            go.Bar(
                name="CrewVote",
                x=role,
                y=[crew_v, 0],
                marker={"color": "rgba(96, 168, 10, 0.7)"},
            ),
            go.Bar(
                name="CrewTask",
                x=role,
                y=[crew_t, 0],
                marker={"color": "rgba(116, 201, 12, 0.7)"},
            ),
            go.Bar(
                name="ImpoKill",
                x=role,
                y=[0, impo_k],
                marker={"color": "rgba(242, 37, 37, 0.7)"},
            ),
            go.Bar(
                name="ImpoVote",
                x=role,
                y=[0, impo_v],
                marker={"color": "rgba(191, 28, 28, 0.7)"},
            ),
            go.Bar(
                name="ImpoSabo",
                x=role,
                y=[0, impo_s],
                marker={"color": "rgba(168, 28, 28, 0.7)"},
            ),
        ]
    )
    fig.update_layout(
        barmode="stack",
        annotations=[
            dict(
                x=0,
                y=crew_v / 2,
                xref="x",
                yref="y",
                text=f"Vote: {crew_v}%",
                showarrow=False,
            ),
            dict(
                x=0,
                y=crew_t / 2 + crew_v,
                xref="x",
                yref="y",
                text=f"Task: {crew_t}%",
                showarrow=False,
            ),
            dict(
                x=1,
                y=impo_k / 2,
                xref="x",
                yref="y",
                text=f"Kill: {impo_k}%",
                showarrow=False,
            ),
            dict(
                x=1,
                y=impo_v / 2 + impo_k,
                xref="x",
                yref="y",
                text=f"Vote: {impo_v}%",
                showarrow=False,
            ),
            dict(
                x=1,
                y=impo_v + impo_k + impo_s / 2,
                xref="x",
                yref="y",
                text=f"Sabotage: {impo_s}%",
                showarrow=False,
            ),
        ],
        showlegend=False,
    )
    fig.update_yaxes(range=[0, 100])
    fig.update_layout(title_text=f"Win Rate: <b>{user_name}", font_size=12)
    fig.update_layout(autosize=False, width=450, height=500)
    #  fig.show()
    fig.write_image(f"temp/fig_winrate_{user_name}.png")


def graph_it(data):
    user = data[0]
    date = data[1]
    stats = ast.literal_eval(data[2])
    user_name = get_name(user)[0]
    user_id = get_name(user)[1]
    """for k, v in stats.items():
        print(f'{k.lower().replace(" ", "_")} = stats.get("{k}")')"""

    bodies_reported = stats.get("Bodies Reported")
    emergencies_called = stats.get("Emergencies Called")
    tasks_completed = stats.get("Tasks Completed")
    all_tasks_completed = stats.get("All Tasks Completed")
    sabotages_fixed = stats.get("Sabotages Fixed")
    impostor_kills = stats.get("Impostor Kills")
    times_murdered = stats.get("Times Murdered")
    times_ejected = stats.get("Times Ejected")
    crewmate_streak = stats.get("Crewmate Streak")
    times_impostor = stats.get("Times Impostor")
    times_crewmate = stats.get("Times Crewmate")
    games_started = stats.get("Games Started")
    games_finished = stats.get("Games Finished")
    impostor_vote_wins = stats.get("Impostor Vote Wins")
    impostor_kill_wins = stats.get("Impostor Kill Wins")
    impostor_sabotage_wins = stats.get("Impostor Sabotage Wins")
    crewmate_vote_wins = stats.get("Crewmate Vote Wins")
    crewmate_task_wins = stats.get("Crewmate Task Wins")

    graph_sankey(
        user_name,
        games_started,
        games_finished,
        times_crewmate,
        times_impostor,
        impostor_vote_wins,
        impostor_kill_wins,
        impostor_sabotage_wins,
        crewmate_vote_wins,
        crewmate_task_wins,
    )
    graph_winratio(
        user_name,
        times_crewmate,
        times_impostor,
        impostor_vote_wins,
        impostor_kill_wins,
        impostor_sabotage_wins,
        crewmate_vote_wins,
        crewmate_task_wins,
    )
