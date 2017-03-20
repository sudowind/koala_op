/**
 * Created by wangfeng on 2017/3/20.
 */
var account = function () {

    return {
        init: function () {
            D('123');

        },
        submit_file: function () {
            var csrf_token = getCookie('csrftoken');
            var file = $('#student_file')[0].files[0];
            // D(file);
            var form = new FormData();
            form.append('csrfmiddlewaretoken', csrf_token);
            form.append('file', file);
            D('upload');
            $.ajax({
                url: 'upload/',
                type: 'post',
                data: form,
                processData: false,
                contentType: false,
                success: function (data) {
                    console.log(data);
                }
            })
        }
    }
}();