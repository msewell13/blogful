from flask import render_template, request, redirect, url_for

from . import app
from .database import session, Entry
from .forms import AddEntry, DeleteEntry

PAGINATE_BY = 10

@app.route('/')
@app.route('/page/<int:page>')
def entries(page=1):
	# Zero - indexed page
	page_index = page - 1

	count = session.query(Entry).count()

	start = page_index * PAGINATE_BY
	end = start + PAGINATE_BY

	total_pages = (count - 1) // PAGINATE_BY + 1
	has_next = page_index < total_pages - 1
	has_prev = page_index > 0

	entries = session.query(Entry)
	entries = entries.order_by(Entry.datetime.desc())
	entries = entries[start:end]

	return render_template('entries.html',
							entries=entries,
							has_next=has_next,
							has_prev=has_prev,
							page=page,
							total_pages=total_pages
							)


@app.route('/entry/add', methods=["GET", "POST"])
def add_entry_post():
	form = AddEntry()
	if form.validate_on_submit():
		entry = Entry(
					title=form.title.data,
					content=form.content.data
					)
		session.add(entry)
		session.commit()
		return redirect(url_for('entries'))
	else:
		return render_template('add_entry.html', form=form)


@app.route('/entry/<int:id>')
def view_entry(id):
	for entry in session.query(Entry):
		if entry.id == id:
			return render_template('view_entry.html', entry=entry)


@app.route('/entry/<int:id>/edit', methods=["GET", "POST"])
def edit_entry(id):
	for entry in session.query(Entry):
		if entry.id == id:
			form = AddEntry(obj=entry)
			if form.validate_on_submit():
				form.populate_obj(entry)
				session.add(entry)
				session.commit()
				return redirect(url_for('entries'))
			return render_template('add_entry.html', form=form)


@app.route('/entry/<int:id>/delete', methods=["GET", "POST"])
def delete_entry(id):
	for entry in session.query(Entry):
		if entry.id == id:
			form = DeleteEntry()
			if form.validate_on_submit():
				session.delete(entry)
				session.commit()
				return redirect(url_for('entries'))
			return render_template('delete_entry.html', entry=entry, form=form)




