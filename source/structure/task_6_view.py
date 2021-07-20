import flask_sijax
from flask import render_template, redirect, url_for, Blueprint, request, g, flash
from source.admin_panel_models import Task, TaskType, Word, TaskWord, Media
from source import db
from source.structure.forms import ButtonAddForm, ButtonDeleteForm, BackButtonForm, RightSentForm, UploadImageForm
from source.static.media_handler import add_to_task_image

task_6_bp = Blueprint('task_6_bp', __name__, url_prefix='/task_6_sent_image', template_folder='templates')


@flask_sijax.route(task_6_bp, '<int:task_id>/', methods=["GET", "POST"])
def render(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task_type = TaskType.query.filter_by(id=task.task_type_id).first()
    task_words_id_list = task.elements.get('words_id')
    task_words = [
        TaskWord(task_id, word) for word in
        [(Word.query.filter_by(id=word_id).first()) for word_id in task_words_id_list]
    ]

    sent_images_id_lst = task.media.get('sent_images_id')
    if sent_images_id_lst:
        sent_images = [Media.query.filter_by(id=id).first() for id in sent_images_id_lst]
    else:
        sent_images=[]

    task_image_form = UploadImageForm()
    if task_image_form.validate_on_submit() and task_image_form.image.data:
        image_media = add_to_task_image(task=task, file=task_image_form.image.data)
        sent_images_id_lst = task.media.get('sent_images_id')
        sent_images_id_lst.append(image_media.id)
        task.media['sent_images_id'] = sent_images_id_lst
        db.session.commit()
        return redirect(url_for('task_6_bp.render', task_id=task.id))

    back_btn = BackButtonForm()
    if back_btn.validate_on_submit() and back_btn.back.data:
        return redirect(url_for('structure.lesson', lesson_id=task.lesson_id))

    sent_form = RightSentForm()
    if sent_form.validate_on_submit() and sent_form.submit.data:
        sent_lang = sent_form.sent_lang_A.data
        sent_lit = sent_form.sent_lit_A.data
        task.right_sentences['sent_lang_A'] = [sent_lang]
        task.right_sentences['sent_lit_A'] = [sent_lit]
        db.session.commit()
        flash('sent_lang update success')
    elif request.method == "GET":
        sent_form.sent_lang_A.data = task.right_sentences.get('sent_lang_A')[0] if task.right_sentences.get(
            'sent_lang_A') else ''
        sent_form.sent_lit_A.data = task.right_sentences.get('sent_lit_A')[0] if task.right_sentences.get(
            'sent_lang_A') else ''


    button_add_word = ButtonAddForm()
    if button_add_word.validate_on_submit() and button_add_word.add.data:
        new_word = Word(char='新', pinyin='xīn', lang='новый')
        db.session.add(new_word)
        db.session.commit()
        return redirect(url_for('elements.word', word_id=new_word.id))

    button_delete_task = ButtonDeleteForm()
    if button_delete_task.validate_on_submit() and button_delete_task.delete.data:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('structure.lesson', lesson_id=task.lesson_id))

    def act_deact_word(obj_response, word_id):
        task = Task.query.filter_by(id=task_id).first()
        active_words = task.elements['words_id_active_or_to_del']
        if word_id in active_words:
            active_words.remove(word_id)
            task.elements['words_id_active_or_to_del'] = active_words
        else:
            active_words.append(word_id)
            task.elements['words_id_active_or_to_del'] = active_words
        db.session.commit()

    search_val = request.args.get('search_key')
    if search_val:
        words = Word.query.filter(
            Word.char.contains(search_val) | Word.pinyin.contains(search_val) | Word.lang.contains(search_val))
    else:
        words = Word.query.all()

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('act_deact_word_req', act_deact_word)
        return g.sijax.process_request()

    return render_template('tasks/6_sent_image.html',
                           task=task, task_type=task_type, sent_images=sent_images,
                           task_image_form=task_image_form, sent_form=sent_form,
                           back_btn=back_btn, button_delete_task=button_delete_task, button_add_word=button_add_word,
                           task_words=task_words,
                           words=words,
                           )