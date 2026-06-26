import { NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'

export async function GET(
  _request: Request,
  { params }: { params: { id: string } }
) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { data: payment, error } = await supabase
    .from('crypto_payments')
    .select('status, confirmed_at, tx_hash')
    .eq('id', params.id)
    .eq('user_id', user.id)
    .single()

  if (error || !payment) {
    return NextResponse.json({ error: 'Payment not found' }, { status: 404 })
  }

  return NextResponse.json({
    status: payment.status,
    confirmedAt: payment.confirmed_at,
    txHash: payment.tx_hash,
  })
}
