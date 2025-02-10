import csv
import io
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Contact

# Function to check if the user is an Editor
def is_editor(user):
    return user.is_authenticated and user.groups.filter(name="editor").exists()

def index(request):
    """ Display and search contacts in a 4-column table. """
    query = request.GET.get('q', '').strip()
    contacts = Contact.objects.all()

    if query:
        contacts = contacts.filter(name__icontains=query)  # Search by name

    # Arrange contacts into pairs (2 columns per row)
    contacts_list = list(contacts)
    contacts_paired = [(contacts_list[i], contacts_list[i+1] if i+1 < len(contacts_list) else None)
                       for i in range(0, len(contacts_list), 2)]

    return render(request, 'contacts/index.html', {'contacts': contacts_paired, 'query': query})

# Custom login page for editors
def editor_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if is_editor(user):  # Check if user is in "Editor" group
                login(request, user)
                return redirect("admin_panel")  # Redirect to contacts admin panel
            else:
                return render(request, "contacts/editor_login.html", {"error": "Access Denied. You are not an Editor."})
        else:
            return render(request, "contacts/editor_login.html", {"error": "Invalid username or password."})

    return render(request, "contacts/editor_login.html")

# Logout view for editors
def editor_logout(request):
    logout(request)
    return redirect("editor_login")  # Redirect to login page after logout

# Protect the admin panel - only logged-in "Editor" users can access
@login_required(login_url="/contacts/admin/login/")  # Redirects unauthenticated users
@user_passes_test(is_editor, login_url="/contacts/admin/login/")
def admin_panel(request):
    """ Single admin panel for managing contacts: add, edit, and delete. """
    if request.method == "POST":
        edit_id = request.POST.get("edit_id")
        delete_id = request.POST.get("delete_id")
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()

        if edit_id:  # Edit Contact
            contact = get_object_or_404(Contact, id=edit_id)
            contact.name, contact.phone = name, phone
            contact.save()

        elif delete_id:  # Delete Contact
            contact = get_object_or_404(Contact, id=delete_id)
            contact.delete()

        elif name and phone:  # Add New Contact
            Contact.objects.create(name=name, phone=phone)

        return redirect("admin_panel")

    contacts = Contact.objects.all()
    return render(request, "contacts/admin.html", {"contacts": contacts})


def download_contacts(request):
    """ Generate and return a CSV file with UTF-8 encoding for Persian text. """
    
    # Create an in-memory buffer for writing CSV data
    output = io.StringIO()
    
    # Use `utf-8-sig` encoding to support Persian text in Excel
    writer = csv.writer(output)
    
    # Write header row
    writer.writerow(["نام مخاطب", "شماره داخلی"])

    # Write contacts data
    for contact in Contact.objects.all():
        writer.writerow([contact.name, contact.phone])

    # Encode output as UTF-8-SIG (so Excel recognizes Persian characters)
    response = HttpResponse(output.getvalue().encode('utf-8-sig'), content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="contacts.csv"'
    
    return response

