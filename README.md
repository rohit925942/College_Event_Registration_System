# Campus Noticeboard — College Event Registration System

A Django web app where college students can create an account, browse events happening
on campus, register for the ones they want to attend, and manage their own profile —
all from one place instead of scattered WhatsApp groups and notices.

---

## Features

- **Student signup & login** — session-based authentication (no third-party auth service)
- **Event listing with search** — browse all events, or search by name
- **Seat-limited registration** — every event has a capacity; once seats run out,
  registration is disabled with a "Full" badge instead of silently overbooking
- **Registration deadline enforcement** — once an event's date has passed, it's marked
  "Event over" and registration is automatically closed — no signing up for events that
  already happened
- **Cancel registration** — students can back out of an upcoming event from "My Events",
  which immediately frees up the seat for someone else
- **My Events** — a student's personal list of everything they've registered for,
  sorted by date, with a "Past" badge on events that have already happened
- **Dashboard** — quick stats: total events, total registrations
- **My Profile** — view account details and edit name / email / password
- **Styled feedback pages** — success/error states (event full, registration closed,
  already registered, login failed, etc.) render as a proper page instead of plain text
- Responsive, single design system across every page ("Campus Noticeboard" theme —
  parchment background, navy ink text, mustard accent, Fraunces + IBM Plex Sans type)

### Problems this solves

| Problem | How it's handled |
|---|---|
| Event halls have limited seats, but nothing stopped overbooking | `Event.capacity` + a live seat count; registration is blocked once full |
| Students could register for events that already happened | Registration closes automatically once `event_date` is in the past |
| A student registers but later can't attend — seat sits wasted | "Cancel" on My Events deletes the registration and frees the seat instantly |
| No way to know how full an event is before registering | Events page shows live "X seats left" / "Only X left" / "Full" badges |
| Duplicate registrations for the same event | Blocked in the view logic *and* enforced by a DB `unique_together` constraint |
| Passwords/records scattered, no self-service account view | "My Profile" page to view and edit account details anytime |

---

## Tech Stack

| Layer          | Technology                          |
|-----------------|--------------------------------------|
| Backend         | Django (Python)                     |
| Database        | SQLite (`db.sqlite3`)               |
| Frontend        | Django Templates + plain CSS        |
| Auth / sessions | Django's built-in session framework (custom `student_id` key, not `django.contrib.auth`) |
| Fonts           | Google Fonts — Fraunces, IBM Plex Sans |

---

## Project Structure

```
College_Event_Registration_System/
├── college_event/            # Project package
│   ├── settings.py           # DB config, installed apps, template dir
│   ├── urls.py                # Root URL routing
│   └── wsgi.py / asgi.py     # Deployment entry points
│
├── event_app/                 # Main app — all the actual logic
│   ├── models.py             # Student, Event, Registration
│   ├── views.py               # All view functions
│   ├── urls.py                 # App-level routes
│   ├── admin.py
│   └── migrations/
│
├── templates/
│   ├── base.html              # Shared layout, nav, design system (all pages extend this)
│   ├── index.html             # Landing page
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── events.html            # Event listing + search
│   ├── my_events.html         # Student's own registrations
│   ├── profile.html           # View / edit account
│   └── message.html           # Reusable styled success/error page
│
├── manage.py
└── db.sqlite3
```

---

## Data Model

**Student**
| Field    | Type                          |
|----------|--------------------------------|
| name     | CharField                     |
| email    | EmailField (`unique=True`)    |
| password | CharField (plain text — see Known Limitations) |

**Event**
| Field        | Type       |
|--------------|------------|
| event_name   | CharField  |
| event_date   | DateField  |
| venue        | CharField  |
| description  | TextField  |
| capacity     | PositiveIntegerField (default 50) — max seats; used to block registration once full |

**Registration** (join table between Student and Event)
| Field         | Type                                   |
|---------------|------------------------------------------|
| student       | ForeignKey → Student (`on_delete=CASCADE`) |
| event         | ForeignKey → Event (`on_delete=CASCADE`)   |
| registered_at | DateTimeField (`auto_now_add=True`) — used to sort "My Events" |

`Meta.unique_together = ('student', 'event')` — this stops a student registering for
the same event twice at the database level, not just in the view.

---

## Routes

| URL                  | View         | Description                                             |
|-----------------------|--------------|-----------------------------------------------------------|
| `/`                   | `home`       | Landing page                                              |
| `/register/`          | `register`   | GET: signup form. POST: creates a Student                |
| `/login/`             | `login`      | GET: login form. POST: authenticates and starts a session |
| `/dashboard/`         | `dashboard`  | Total events / registrations                              |
| `/events/`            | `events`     | Event listing, `?search=` filters by name                 |
| `/join/<event_id>/`   | `join_event` | Registers the logged-in student for an event (blocked if full or past deadline) |
| `/cancel/<event_id>/` | `cancel_registration` | Cancels the logged-in student's registration, freeing the seat |
| `/my-events/`         | `my_events`  | Logged-in student's own registrations                      |
| `/profile/`           | `profile`    | View / edit the logged-in student's account                 |
| `/logout/`            | `logout`     | Clears the session                                          |

---

## Setup & Run Locally

**Requirements:** Python 3.10+ and pip.

```bash
# 1. Extract the project and move into it
cd College_Event_Registration_System

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 4. Install Django
pip install django

# 5. Apply migrations (creates db.sqlite3 tables)
python manage.py migrate

# 6. (Optional) create an admin user, to add events via /admin/
python manage.py createsuperuser

# 7. Run the dev server
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

To add events, log into **http://127.0.0.1:8000/admin/** with the superuser account
created above and add `Event` entries — there's currently no in-app UI for creating
events, only for browsing and registering.

---

## Known Limitations

- Passwords are stored as plain text, not hashed — fine for a class project, **not**
  production-ready. Fix: use `django.contrib.auth.hashers.make_password` /
  `check_password`, or switch to Django's built-in `User` model entirely.
- Login uses a hand-rolled `request.session['student_id']` key rather than
  `django.contrib.auth` — no permissions system, no password-reset flow.
- No in-app UI to create/edit/delete events — only Django's default `/admin/` panel.
- No pagination on the event list.

---

## Possible Next Steps

- Hash passwords / move to Django's auth system
- Add an event-management UI for admins/organisers
- Add pagination and category filters to the events page
- Email confirmation on signup
