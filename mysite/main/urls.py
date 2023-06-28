from django.urls import path

from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("dashboard",views.dashboard, name="dashboard"),
    path("sign",views.sign_in_up, name="signinup"),
    path("yourwork",views.your_work, name="your-work"),
    path("leaderboard",views.leaderboard, name="leaderboard"),
    path("profile",views.profile, name="profile"),
    path("notes",views.notes_view, name="notes"),
    path("admindashboard",views.admin, name="admin"),
    path("edit-profile",views.edit_profile, name="edit_profile"),
    path("preview",views.preview, name="preview"),
    path("reward",views.reward, name="reward"),
    path("logout",views.logout, name="logout"),
    path("admin-login",views.adminlogin, name="admin-login"),
    path("adminlogout",views.adminlogout, name="adminlogout"),

]